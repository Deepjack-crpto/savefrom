import os
import html
import re

base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | SaveFrom</title>
    <meta name="description" content="{description}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a26;
            --bg-card-hover: #222233;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: rgba(255,255,255,0.06);
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex; flex-direction: column;
            overflow-x: hidden;
            line-height: 1.6;
        }}
        .bg-gradient {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: 
                radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59,130,246,0.12) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.08) 0%, transparent 50%);
            pointer-events: none; z-index: 0;
        }}
        header {{
            position: sticky; top: 0; z-index: 100;
            padding: 1rem 1.5rem;
            background: rgba(10,10,15,0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
        }}
        .header-content {{
            max-width: 900px; margin: 0 auto;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .logo {{
            font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-decoration: none;
        }}
        main {{
            position: relative; z-index: 1; flex: 1;
            max-width: 900px; margin: 0 auto; padding: 3rem 1.5rem 4rem; width: 100%;
        }}
        .content-card {{
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 16px; padding: 2.5rem;
        }}
        .content-card h1 {{ font-size: 2.5rem; margin-bottom: 1.5rem; font-weight: 800; }}
        .content-card h2 {{ font-size: 1.5rem; margin: 2rem 0 1rem; color: var(--accent-cyan); }}
        .content-card p {{ margin-bottom: 1rem; color: var(--text-secondary); }}
        .content-card ul, .content-card ol {{ margin-bottom: 1rem; padding-left: 1.5rem; color: var(--text-secondary); }}
        .content-card li {{ margin-bottom: 0.5rem; }}
        .content-card a {{ color: var(--accent-blue); text-decoration: none; }}
        .content-card a:hover {{ text-decoration: underline; }}
        
        /* Footer */
        footer {{
            position: relative; z-index: 1;
            text-align: center; padding: 3rem 1.5rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted); font-size: 0.85rem;
            background: var(--bg-card);
        }}
        .footer-links {{
            display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .footer-links a {{
            color: var(--text-primary); text-decoration: none; font-weight: 500;
            transition: color 0.3s;
        }}
        .footer-links a:hover {{ color: var(--accent-blue); }}
        footer p {{ margin-bottom: 0.5rem; max-width: 600px; margin-left: auto; margin-right: auto; }}
        
        .blog-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
        .blog-item {{ background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border); transition: transform 0.2s; }}
        .blog-item:hover {{ transform: translateY(-3px); border-color: var(--accent-blue); }}
        .blog-item h3 {{ font-size: 1.1rem; margin-bottom: 0.5rem; }}
        .blog-item a {{ color: var(--text-primary); text-decoration: none; font-weight: 600; display: block; }}
        .blog-item p {{ font-size: 0.9rem; margin-bottom: 1rem; }}
        .read-more {{ color: var(--accent-blue) !important; font-size: 0.9rem; }}
        
        @media (max-width: 768px) {{
            .content-card {{ padding: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <header>
        <div class="header-content">
            <a href="/savefrom.html" class="logo">SaveFrom</a>
            <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-muted);">Fast, Simple & Secure Media Access</div>
        </div>
    </header>
    <main>
        <div class="content-card">
            {content}
        </div>
    </main>
    <footer>
        <div class="footer-links">
            <a href="/savefrom.html">Home</a>
            <a href="/about.html">About Us</a>
            <a href="/contact.html">Contact Us</a>
            <a href="/privacy-policy.html">Privacy Policy</a>
            <a href="/terms.html">Terms & Conditions</a>
            <a href="/disclaimer.html">Disclaimer</a>
            <a href="/faq.html">FAQ</a>
            <a href="/blog.html">Blog</a>
        </div>
        <p>SaveFrom · Fast, Simple & Secure Media Access</p>
        <p>SaveFrom does not host or store any media on its servers. We respect copyright laws and provide tool for personal, non-commercial use only. Do not bypass DRM or access unauthorized/paywalled content.</p>
        <p style="margin-top: 0.75rem; font-weight: 600; font-size: 0.85rem; color: var(--accent-blue); letter-spacing: 1px;">DEVELOPED BY DEEPAK MOHANRAJ</p>
    </footer>
</body>
</html>
"""

pages = {
    "privacy-policy.html": {
        "title": "Privacy Policy",
        "description": "Privacy Policy for SaveFrom. Understand how we handle your data, ensuring a fast, simple, and secure experience.",
        "content": """
            <h1>Privacy Policy</h1>
            <p>Last updated: June 12, 2026</p>
            <p>At SaveFrom, we respect your privacy. This Privacy Policy outlines the types of personal information that is received and collected by our website and how it is used.</p>
            <h2>Information Collection and Use</h2>
            <p>We do not require users to create an account or provide personal information to use our core downloading services. We may collect non-personally identifiable information such as browser type, operating system, and IP address for analytical purposes to improve our service.</p>
            <h2>Cookies</h2>
            <p>SaveFrom uses cookies to store information about visitors' preferences and to improve the user experience. Cookies help us understand how our site is being used, enabling us to optimize our web pages. We also show a cookie consent banner ensuring compliance with modern privacy standards.</p>
            <h2>AdSense and Third-Party Advertising</h2>
            <p>We may use third-party advertising companies, such as Google AdSense, to serve ads when you visit our website. These companies may use information (not including your name, address, email address, or telephone number) about your visits to this and other websites in order to provide advertisements about goods and services of interest to you. Google uses the DoubleClick cookie to serve interest-based advertising.</p>
            <h2>Data Security</h2>
            <p>We implement appropriate security measures to protect against unauthorized access to or unauthorized alteration, disclosure, or destruction of data. However, remember that no method of transmission over the internet is 100% secure.</p>
            <h2>Changes to This Privacy Policy</h2>
            <p>We may update our Privacy Policy from time to time. Thus, we advise you to review this page periodically for any changes. We will notify you of any changes by posting the new Privacy Policy on this page.</p>
        """
    },
    "terms.html": {
        "title": "Terms & Conditions",
        "description": "Terms and Conditions of use for SaveFrom. Read our guidelines for using our media downloading tool.",
        "content": """
            <h1>Terms & Conditions</h1>
            <p>Last updated: June 12, 2026</p>
            <h2>1. Acceptance of Terms</h2>
            <p>By accessing and using SaveFrom, you accept and agree to be bound by the terms and provision of this agreement.</p>
            <h2>2. Permitted Use</h2>
            <p>SaveFrom is provided as a tool to facilitate the downloading of publicly accessible media for personal, non-commercial use only. You agree to use the tool only in ways that are compliant with all applicable laws and regulations.</p>
            <h2>3. Copyright compliance</h2>
            <p>We absolutely respect the intellectual property rights of others. SaveFrom does not permit the downloading of copyrighted material without the explicit permission of the copyright owner. By using our tool, you confirm that you have the right to download the content in question. SaveFrom does not host any media files; it functions strictly as a client-side conduit.</p>
            <h2>4. Restrictions</h2>
            <ul>
                <li>You may not use the service to bypass authentication mechanisms, DRM, paywalls, or any access controls.</li>
                <li>You may not exploit our platform to facilitate copyright infringement.</li>
                <li>We reserve the right to block certain URLs or domains that consistently violate intellectual property rights.</li>
            </ul>
            <h2>5. Disclaimer of Warranties</h2>
            <p>The service is provided \"as is\" without any warranty. We do not guarantee continuous, uninterrupted, or secure access to our service.</p>
        """
    },
    "disclaimer.html": {
        "title": "Disclaimer",
        "description": "Disclaimer for SaveFrom. Read about our legal policies and copyright compliance.",
        "content": """
            <h1>Disclaimer</h1>
            <p>SaveFrom provides a web-based utility that extracts download links from various public media platforms. The tool is intended strictly for personal, private, and fair use purposes.</p>
            <h2>No Hosting of Content</h2>
            <p>SaveFrom does not host, store, or caching any video or audio files on its servers. All files are downloaded directly from the content distribution networks (CDNs) of the respective platforms. Our service merely acts as an intermediary, querying the platform and returning the direct video stream URLs.</p>
            <h2>Respect for Copyright</h2>
            <p>We do not promote, encourage, or facilitate piracy. We explicitly forbid the use of SaveFrom for downloading copyrighted or DRM-protected materials without the permission of the intellectual property owner. It is the user's sole responsibility to ensure they have the lawful right to download and use the media.</p>
            <h2>Non-affiliation</h2>
            <p>SaveFrom is an independent entity and is not affiliated with, endorsed by, or sponsored by YouTube, TikTok, Instagram, Twitter, or any other media platform. All trademarks, logos, and brands belong to their respective owners.</p>
        """
    },
    "about.html": {
        "title": "About Us",
        "description": "Learn more about SaveFrom, our mission, and why we are the fastest and simplest media access tool.",
        "content": """
            <h1>About Us</h1>
            <p>Welcome to <strong>SaveFrom</strong> – Fast, Simple & Secure Media Access.</p>
            <p>We built SaveFrom to solve a simple problem: making publicly available web media easily accessible for offline, personal use. Whether you are an educator needing a video for a presentation, a user saving a memorable clip, or simply want to listen to a non-copyrighted track offline, SaveFrom is designed for you.</p>
            <h2>Our Mission</h2>
            <p>To provide an exceptionally fast, bloat-free, and incredibly user-friendly utility for safely accessing online media. We strive to maintain a high-quality aesthetic combined with robust backend engineering.</p>
            <h2>Why Choose Us?</h2>
            <ul>
                <li><strong>No Registration Required:</strong> Jump straight into downloading without any annoying sign-ups.</li>
                <li><strong>Fast Processing:</strong> We utilize state-of-the-art backend tools like yt-dlp to extract the highest quality streams efficiently.</li>
                <li><strong>Safe and Secure:</strong> Privacy is our priority. We do not track your downloads or mandate invasive software installations.</li>
            </ul>
            <h2>Developed With Care</h2>
            <p>SaveFrom is proudly developed by Deepak Mohanraj, ensuring continuous updates, premium design aesthetics, and a focus on optimal user experience.</p>
        """
    },
    "contact.html": {
        "title": "Contact Us",
        "description": "Get in touch with the SaveFrom team for support, feedback, or business inquiries.",
        "content": """
            <h1>Contact Us</h1>
            <p>We'd love to hear from you. If you have any questions, feedback, or issues regarding SaveFrom, please reach out to us!</p>
            <h2>Support & Inquiries</h2>
            <p>For general inquiries, bug reports, and DMCA takedown requests, you can reach us at:</p>
            <p><strong>Email:</strong> contact@savefrom-demo.com</p>
            <h2>DMCA Policy</h2>
            <p>If you believe your copyrighted work has been infringed by a user of our service, please contact us immediately. Since we do not host any files, we are limited to blocking specific URLs from being processed by our system. Please provide the URL in question along with proof of copyright ownership.</p>
            <h2>Business & Advertising</h2>
            <p>Interested in advertising with us or discussing a potential partnership? Let us know! Our platform provides great reach, especially considering our AdSense-ready robust architecture.</p>
        """
    },
    "faq.html": {
        "title": "Frequently Asked Questions",
        "description": "Common questions and answers about using SaveFrom.",
        "content": """
            <h1>Frequently Asked Questions (FAQ)</h1>
            <h2>Is SaveFrom completely free?</h2>
            <p>Yes, SaveFrom is 100% free to use. You do not need to pay anything or register for an account.</p>
            <h2>Which platforms are supported?</h2>
            <p>We support all major platforms including YouTube, TikTok, Twitter/X, Instagram, Facebook, and hundreds of other websites. If it's a public video, chances are we can download it.</p>
            <h2>Can I download live streams?</h2>
            <p>No, SaveFrom is designed to download standard, completed video and audio files. Live streams typically cannot be downloaded until they have concluded and are published as VODs.</p>
            <h2>Is it legal to download videos?</h2>
            <p>It is legal to download videos for personal, fair use (e.g., watching offline). However, you respect copyright laws. Do not use downloaded videos for commercial purposes or distribute them if they are copyrighted.</p>
            <h2>Where are my files saved?</h2>
            <p>By default, the files are saved in your device's \"Downloads\" folder. You can usually change this in your browser settings.</p>
            <h2>Do you keep logs of what I download?</h2>
            <p>No. We process the request and deliver the link. We do not store histories of your downloads.</p>
        """
    }
}

# Add 10 Blog Articles Data
blog_articles = [
    {
        "slug": "how-to-download-youtube-videos",
        "title": "How to Download YouTube Videos Safely and Free",
        "desc": "A comprehensive guide on securely saving YouTube videos for offline viewing.",
        "content": "<h1>How to Download YouTube Videos Safely and Free</h1><p>Downloading content from YouTube is incredibly useful when traveling or lacking internet access. While many tools exist, it's vital to choose one that respects your device's security.</p><h2>Use SaveFrom for Speed</h2><p>Our platform handles 1080p, 4K, and high-quality audio extraction without mandating external app downloads. Just copy the YouTube URL, paste it into our search bar, and click 'Analyze'. Within seconds, you'll see all available formats.</p><h2>Is it Legal?</h2><p>Remember that downloading copyrighted content without permission violates YouTube's Terms of Service. Always stick to personal/fair use, or download videos licensed under Creative Commons.</p>"
    },
    {
        "slug": "best-tiktok-downloader-no-watermark",
        "title": "The Ultimate TikTok Downloader: High Quality",
        "desc": "Learn how to save your favorite TikToks easily in high resolution.",
        "content": "<h1>The Ultimate TikTok Downloader: High Quality</h1><p>TikTok is the internet's most fast-paced viral platform. Have you ever seen a hilarious video, only for it to be deleted the next day? Saving them is the best way to archive your favorite content.</p><h2>How to Save TikToks</h2><p>On your mobile app, tap the 'Share' arrow, then select 'Copy Link'. Head over to SaveFrom, paste your link, and download the MP4 version directly to your camera roll.</p><h2>Tips for Creators</h2><p>If you are a creator, retaining high-quality copies of your early works before applying in-app filters or heavy edits can be beneficial for crossposting to YouTube Shorts or Instagram Reels.</p>"
    },
    {
        "slug": "extract-audio-from-video",
        "title": "How to Extract Audio from Any Video Link",
        "desc": "Step-by-step tutorial on converting video links into MP3 audio files.",
        "content": "<h1>How to Extract Audio from Any Video Link</h1><p>Sometimes you don't need the visuals; you just want a podcast episode, a public domain music track, or an interview in audio format to save bandwidth and listen on the go.</p><h2>How It Works</h2><p>SaveFrom features a dedicated 'Download Audio' option. Our robust backend processes the media and extracts the highest available audio bitrate (up to 320kbps MP3). Just input the link, and choose the audio download card.</p><h2>Why Not Just Screen Record?</h2><p>Screen recording severely compresses audio quality. Native extraction ensures crisp, lossless (or near-lossless) audio.</p>"
    },
    {
        "slug": "why-use-yt-dlp",
        "title": "Understanding yt-dlp: The Tech Behind the Magic",
        "desc": "A technical look at why yt-dlp powers the best media downloaders online.",
        "content": "<h1>Understanding yt-dlp: The Tech Behind the Magic</h1><p>If you're wondering how SaveFrom provides such fast and accurate media analysis, it's largely thanks to the open-source community, specifically yt-dlp.</p><h2>What is yt-dlp?</h2><p>yt-dlp is a command-line tool that acts as a fork of the popular youtube-dl. It features rapid updates, bypassing modern rate limits, and immense platform support.</p><h2>How SaveFrom Uses It</h2><p>We wrap this powerful utility in a beautiful, modern, responsive UI. You get all the power of hardcore command-line tools without needing to open a terminal.</p>"
    },
    {
        "slug": "downloading-twitter-videos",
        "title": "Saving Twitter (X) Videos to Your Phone",
        "desc": "A quick guide on safely downloading Twitter/X videos and GIFs.",
        "content": "<h1>Saving Twitter (X) Videos to Your Phone</h1><p>Twitter (now X) makes it notoriously difficult to save videos natively. Often, you're restricted to bookmarking them, which relies on the original poster not deleting their tweet.</p><h2>The Solution</h2><p>SaveFrom flawlessly parses Twitter video links. Tap the share button on the tweet, copy the link, and paste it into our platform. We'll find the underlying MP4 file and present it to you for instant download.</p>"
    },
    {
        "slug": "offline-media-for-travel",
        "title": "Preparing Your Media Library for Long Flights",
        "desc": "Tips on building an offline library before travelling.",
        "content": "<h1>Preparing Your Media Library for Long Flights</h1><p>In-flight Wi-Fi is expensive and often too slow for smooth streaming. Preparing your devices ahead of time is the best travel hack.</p><h2>Batch Downloading</h2><p>Consider accumulating links to documentaries, tech talks, or long-form podcasts. Use SaveFrom to convert these into a local folder on your tablet or laptop. Organize them logically so you don't need an internet connection to browse your newly curated library.</p>"
    },
    {
        "slug": "instagram-reels-download",
        "title": "Guide to Archiving Instagram Reels",
        "desc": "How to save Instagram Reels for offline reference and inspiration.",
        "content": "<h1>Guide to Archiving Instagram Reels</h1><p>Instagram Reels are a goldmine for quick recipes, workout routines, and DIY guides. But what happens when you're at the gym with bad reception?</p><h2>Archiving Made Easy</h2><p>Saving these clips locally means zero buffering. Open Instagram, click the three dots on the Reel, and hit 'Copy Link'. Paste it into SaveFrom. You'll get the high-definition MP4 directly to your device.</p>"
    },
    {
        "slug": "understanding-bitrates-resolutions",
        "title": "Video Quality Explained: 1080p, 4K, and Bitrates",
        "desc": "Understand what different video qualities mean before you download.",
        "content": "<h1>Video Quality Explained: 1080p, 4K, and Bitrates</h1><p>When you paste a link into SaveFrom, you're often given multiple format choices. Which should you pick?</p><h2>Resolutions</h2><p>1080p (Full HD) is generally the sweet spot for mobile and laptop viewing, offering great clarity without massive file sizes. 4K is ideal for TVs but will consume massive amounts of storage.</p><h2>Bitrate</h2><p>Bitrate matters just as much as resolution. Higher bitrates mean less compression artifacts (blocky pixels). SaveFrom prioritizes fetching the 'Best' quality by default.</p>"
    },
    {
        "slug": "protecting-against-malware",
        "title": "How to Avoid Fake Download Buttons",
        "desc": "Stay safe online by recognizing deceptive ads and fake buttons.",
        "content": "<h1>How to Avoid Fake Download Buttons</h1><p>Many competitor sites are littered with deceptive 'Download Now' buttons that lead to malware or unwanted browser extensions.</p><h2>The SaveFrom Promise</h2><p>We utilize a clean, AdSense-friendly, premium UI. Our buttons clearly state exactly what they do (e.g., 'Download Video' or 'Download Audio'). We will never trick you into installing exe files or fishy software. You always get exactly what you asked for: media files.</p>"
    },
    {
        "slug": "educational-fair-use",
        "title": "Using Online Videos for Educational Purposes",
        "desc": "A look at fair use when downloading videos for school or research.",
        "content": "<h1>Using Online Videos for Educational Purposes</h1><p>Educators frequently need to present media in classrooms where internet access might be restricted or blocked by robust firewalls.</p><h2>Fair Use</h2><p>Downloading a portion of a public video to critique, teach, or study often falls under 'Fair Use'. SaveFrom empowers teachers and students to acquire these materials cleanly and efficiently. Always credit the original creator in your presentations!</p>"
    }
]

# Generate blog index
blog_index_content = "<h1>Blog & Guides</h1><p>Read our latest articles on media downloading, tips, and tutorials.</p><div class='blog-grid'>"
for article in blog_articles:
    blog_index_content += f"<div class='blog-item'><h3><a href='/blog/{article['slug']}.html'>{article['title']}</a></h3><p>{article['desc']}</p><a class='read-more' href='/blog/{article['slug']}.html'>Read Article &rarr;</a></div>"
blog_index_content += "</div>"

pages["blog.html"] = {
    "title": "Blog & Guides",
    "description": "Read the latest tips, tutorials, and news about video downloading on the SaveFrom blog.",
    "content": blog_index_content
}

# Write pages
out_dir = "d:/SF"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(os.path.join(out_dir, "blog"), exist_ok=True)

for filename, data in pages.items():
    filepath = os.path.join(out_dir, filename)
    html_out = base_template.format(title=data['title'], description=data['description'], content=data['content'])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_out)

# Write blog articles
for article in blog_articles:
    filepath = os.path.join(out_dir, "blog", f"{article['slug']}.html")
    # need relative path adjustments for footer links
    article_template = base_template.replace('href="/', 'href="/') 
    html_out = article_template.format(title=article['title'], description=article['desc'], content=article['content'])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_out)

print("HTML Pages Generated.")
