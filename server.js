const express = require('express');
const cors = require('cors');
const { execFile, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const app = express();
const PORT = 3000;

// Tool paths
const YT_DLP = 'C:\\Users\\user\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts\\yt-dlp.exe';
const FFMPEG_DIR = 'C:\\Users\\user\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.1.1-full_build\\bin';

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Downloads directory
// Use os.tmpdir() which resolves to /tmp on Vercel and %TEMP% on Windows
const DOWNLOADS_DIR = process.env.VERCEL ? '/tmp' : os.tmpdir();

// Helper: run yt-dlp with args
function runYtDlp(args) {
    return new Promise((resolve, reject) => {
        const env = { ...process.env, PATH: FFMPEG_DIR + ';' + process.env.PATH };
        execFile(YT_DLP, args, { env, maxBuffer: 10 * 1024 * 1024, timeout: 60000 }, (err, stdout, stderr) => {
            if (err) {
                reject(new Error(stderr || err.message));
            } else {
                resolve(stdout);
            }
        });
    });
}

// ============== API: Get media info ==============
app.post('/api/info', async (req, res) => {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'URL is required' });

    try {
        const args = [
            '--dump-json',
            '--no-download',
            '--no-warnings',
            '--no-playlist',
            url
        ];
        const stdout = await runYtDlp(args);
        const info = JSON.parse(stdout);

        // Build format list
        const formats = (info.formats || [])
            .filter(f => f.url || f.manifest_url)
            .map(f => ({
                format_id: f.format_id,
                ext: f.ext,
                resolution: f.resolution || (f.height ? `${f.width}x${f.height}` : 'audio only'),
                height: f.height || 0,
                width: f.width || 0,
                filesize: f.filesize || f.filesize_approx || 0,
                vcodec: f.vcodec || 'none',
                acodec: f.acodec || 'none',
                fps: f.fps || 0,
                tbr: f.tbr || 0,
                abr: f.abr || 0,
                has_video: f.vcodec && f.vcodec !== 'none',
                has_audio: f.acodec && f.acodec !== 'none',
                format_note: f.format_note || ''
            }));

        // Get best video qualities
        const videoFormats = formats
            .filter(f => f.has_video)
            .sort((a, b) => (b.height || 0) - (a.height || 0));

        const audioFormats = formats
            .filter(f => f.has_audio && !f.has_video)
            .sort((a, b) => (b.abr || 0) - (a.abr || 0));

        // Unique video qualities
        const seenHeights = new Set();
        const uniqueVideoFormats = [];
        for (const f of videoFormats) {
            const h = f.height;
            if (h && !seenHeights.has(h)) {
                seenHeights.add(h);
                uniqueVideoFormats.push(f);
            }
        }

        const response = {
            title: info.title || 'Unknown',
            description: (info.description || '').substring(0, 300),
            duration: info.duration || 0,
            duration_string: info.duration_string || '0:00',
            thumbnail: info.thumbnail || '',
            uploader: info.uploader || info.channel || 'Unknown',
            upload_date: info.upload_date || '',
            view_count: info.view_count || 0,
            like_count: info.like_count || 0,
            webpage_url: info.webpage_url || url,
            extractor: info.extractor || 'unknown',
            resolution: info.resolution || `${info.width || 0}x${info.height || 0}`,
            fps: info.fps || 0,
            video_formats: uniqueVideoFormats.slice(0, 8),
            audio_formats: audioFormats.slice(0, 5),
            all_format_count: formats.length
        };

        res.json(response);
    } catch (err) {
        console.error('Info error:', err.message);
        res.status(500).json({ error: 'Failed to fetch media info. ' + err.message });
    }
});

// ============== API: Download video ==============
app.get('/api/download/video', async (req, res) => {
    const { url, quality } = req.query;
    if (!url) return res.status(400).json({ error: 'URL is required' });

    try {
        // First get info for filename
        const infoArgs = ['--dump-json', '--no-download', '--no-warnings', '--no-playlist', url];
        const infoStdout = await runYtDlp(infoArgs);
        const info = JSON.parse(infoStdout);
        
        // Sanitize title for filename
        const safeTitle = (info.title || 'video')
            .replace(/[<>:"\/\\|?*]/g, '')
            .replace(/\s+/g, '_')
            .substring(0, 100);

        const outputFilename = `${safeTitle}.mp4`;

        // Build format selector based on quality
        let formatSelector;
        if (quality && quality !== 'best') {
            formatSelector = `bestvideo[height<=${quality}]+bestaudio/best[height<=${quality}]/best`;
        } else {
            formatSelector = 'bestvideo+bestaudio/best';
        }

        const tempFile = path.join(DOWNLOADS_DIR, `temp_${Date.now()}.mp4`);
        const env = { ...process.env, PATH: FFMPEG_DIR + ';' + process.env.PATH };
        
        const args = [
            '-f', formatSelector,
            '--merge-output-format', 'mp4',
            '--no-playlist',
            '--no-warnings',
            '-o', tempFile,
            '--ffmpeg-location', FFMPEG_DIR,
            url
        ];

        console.log(`[DOWNLOAD VIDEO] Starting: ${safeTitle}`);
        
        const proc = spawn(YT_DLP, args, { env });
        
        let stderr = '';
        proc.stderr.on('data', (d) => { stderr += d.toString(); });
        proc.stdout.on('data', (d) => { console.log('[yt-dlp]', d.toString().trim()); });

        proc.on('close', (code) => {
            if (code !== 0) {
                console.error('[DOWNLOAD ERROR]', stderr);
                // Clean up
                try { fs.unlinkSync(tempFile); } catch(e) {}
                return res.status(500).json({ error: 'Download failed: ' + stderr.substring(0, 200) });
            }

            if (!fs.existsSync(tempFile)) {
                return res.status(500).json({ error: 'Download completed but file not found' });
            }

            const stat = fs.statSync(tempFile);
            console.log(`[DOWNLOAD COMPLETE] ${outputFilename} (${(stat.size / 1024 / 1024).toFixed(1)} MB)`);

            res.setHeader('Content-Disposition', `attachment; filename="${encodeURIComponent(outputFilename)}"`);
            res.setHeader('Content-Type', 'video/mp4');
            res.setHeader('Content-Length', stat.size);

            const stream = fs.createReadStream(tempFile);
            stream.pipe(res);
            stream.on('end', () => {
                // Clean up temp file
                try { fs.unlinkSync(tempFile); } catch(e) {}
            });
            stream.on('error', (err) => {
                console.error('[STREAM ERROR]', err);
                try { fs.unlinkSync(tempFile); } catch(e) {}
                if (!res.headersSent) res.status(500).json({ error: 'Stream error' });
            });
        });

        proc.on('error', (err) => {
            console.error('[PROC ERROR]', err);
            res.status(500).json({ error: 'Failed to start download: ' + err.message });
        });

    } catch (err) {
        console.error('[ERROR]', err.message);
        res.status(500).json({ error: err.message });
    }
});

// ============== API: Download audio ==============
app.get('/api/download/audio', async (req, res) => {
    const { url } = req.query;
    if (!url) return res.status(400).json({ error: 'URL is required' });

    try {
        // First get info for filename
        const infoArgs = ['--dump-json', '--no-download', '--no-warnings', '--no-playlist', url];
        const infoStdout = await runYtDlp(infoArgs);
        const info = JSON.parse(infoStdout);
        
        const safeTitle = (info.title || 'audio')
            .replace(/[<>:"\/\\|?*]/g, '')
            .replace(/\s+/g, '_')
            .substring(0, 100);

        const outputFilename = `${safeTitle}.mp3`;
        const tempFile = path.join(DOWNLOADS_DIR, `temp_audio_${Date.now()}.mp3`);
        const env = { ...process.env, PATH: FFMPEG_DIR + ';' + process.env.PATH };

        const args = [
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', '0',
            '--no-playlist',
            '--no-warnings',
            '-o', tempFile,
            '--ffmpeg-location', FFMPEG_DIR,
            url
        ];

        console.log(`[DOWNLOAD AUDIO] Starting: ${safeTitle}`);

        const proc = spawn(YT_DLP, args, { env });
        
        let stderr = '';
        proc.stderr.on('data', (d) => { stderr += d.toString(); });
        proc.stdout.on('data', (d) => { console.log('[yt-dlp audio]', d.toString().trim()); });

        proc.on('close', (code) => {
            if (code !== 0) {
                console.error('[AUDIO ERROR]', stderr);
                try { fs.unlinkSync(tempFile); } catch(e) {}
                return res.status(500).json({ error: 'Audio download failed: ' + stderr.substring(0, 200) });
            }

            // yt-dlp may append .mp3 to the output
            let finalFile = tempFile;
            if (!fs.existsSync(finalFile) && fs.existsSync(tempFile + '.mp3')) {
                finalFile = tempFile + '.mp3';
            }
            // Also check without double extension
            const noExt = tempFile.replace(/\.mp3$/, '');
            if (!fs.existsSync(finalFile) && fs.existsSync(noExt + '.mp3')) {
                finalFile = noExt + '.mp3';
            }

            if (!fs.existsSync(finalFile)) {
                // Try to find any recently created mp3 in downloads
                const files = fs.readdirSync(DOWNLOADS_DIR)
                    .filter(f => f.startsWith('temp_audio_') && f.endsWith('.mp3'))
                    .map(f => ({ name: f, time: fs.statSync(path.join(DOWNLOADS_DIR, f)).mtimeMs }))
                    .sort((a, b) => b.time - a.time);
                if (files.length > 0) {
                    finalFile = path.join(DOWNLOADS_DIR, files[0].name);
                } else {
                    return res.status(500).json({ error: 'Audio download completed but file not found' });
                }
            }

            const stat = fs.statSync(finalFile);
            console.log(`[AUDIO COMPLETE] ${outputFilename} (${(stat.size / 1024 / 1024).toFixed(1)} MB)`);

            res.setHeader('Content-Disposition', `attachment; filename="${encodeURIComponent(outputFilename)}"`);
            res.setHeader('Content-Type', 'audio/mpeg');
            res.setHeader('Content-Length', stat.size);

            const stream = fs.createReadStream(finalFile);
            stream.pipe(res);
            stream.on('end', () => {
                try { fs.unlinkSync(finalFile); } catch(e) {}
            });
            stream.on('error', (err) => {
                console.error('[STREAM ERROR]', err);
                try { fs.unlinkSync(finalFile); } catch(e) {}
                if (!res.headersSent) res.status(500).json({ error: 'Stream error' });
            });
        });

        proc.on('error', (err) => {
            console.error('[PROC ERROR]', err);
            res.status(500).json({ error: 'Failed to start audio download: ' + err.message });
        });

    } catch (err) {
        console.error('[ERROR]', err.message);
        res.status(500).json({ error: err.message });
    }
});

// ============== API: Health check ==============
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', ytdlp: YT_DLP, ffmpeg: FFMPEG_DIR });
});

// Get LAN IP for mobile access
function getLanIP() {
    const nets = os.networkInterfaces();
    for (const name of Object.keys(nets)) {
        for (const net of nets[name]) {
            if (net.family === 'IPv4' && !net.internal) {
                return net.address;
            }
        }
    }
    return 'localhost';
}

app.listen(PORT, '0.0.0.0', () => {
    if (process.env.VERCEL) return;
    const lanIP = getLanIP();
    console.log(`\n🚀 SaveFrom server running!`);
    console.log(`   PC:     http://localhost:${PORT}/savefrom.html`);
    console.log(`   Mobile: http://${lanIP}:${PORT}/savefrom.html`);
    console.log(`\n   yt-dlp: ${YT_DLP}`);
    console.log(`   ffmpeg: ${FFMPEG_DIR}\n`);
});

module.exports = app;
