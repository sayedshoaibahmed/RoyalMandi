import os
import re

blog_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{seo_title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://royalmandihouse.in/{filename}">
    <meta name="theme-color" content="#D4A017">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="{image}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://royalmandihouse.in/{filename}">
    
    <!-- Preconnect to Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;700&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;700&display=swap">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <style>
        /* CSS Variables */
        :root {
            --color-gold: #D4A017;
            --color-gold-light: #E8B84B;
            --color-black: #0A0A0A;
            --color-black-card: #111111;
            --color-white: #FFFFFF;
            --color-text-muted: #AAAAAA;
            
            --font-heading: 'Playfair Display', Georgia, serif;
            --font-body: 'Inter', Arial, sans-serif;
            
            --transition-fast: 0.2s ease;
            --transition-med: 0.4s ease;
            --transition-slow: 0.4s ease;
            
            --border-radius: 8px;
            --max-width: 1200px;
            --section-padding: 80px 0;
            --section-padding-mobile: 50px 0;
            
            --navbar-height: 80px;
        }

        /* Reset & Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: var(--font-body);
            background-color: var(--color-black);
            color: var(--color-white);
            line-height: 1.6;
            overflow-x: hidden;
            max-width: 100vw;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-heading);
            line-height: 1.2;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        ul {
            list-style: none;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
        }

        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            padding: 14px 32px;
            min-height: 44px;
            font-family: var(--font-body);
            font-weight: 600;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: var(--transition-fast);
            text-transform: uppercase;
            font-size: 15px;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        @media (max-width: 767px) {
            .btn {
                padding: 12px 24px;
                font-size: 14px;
            }
        }

        .btn-primary {
            background-color: var(--color-gold);
            color: #000000;
            border: none;
        }

        .btn-primary:hover {
            background-color: var(--color-gold-light);
            transform: translateY(-2px);
        }

        .btn-outline {
            background-color: transparent;
            color: var(--color-gold);
            border: 2px solid var(--color-gold);
        }
        
        .btn-outline::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: var(--color-gold);
            z-index: -1;
            transform: scaleX(0);
            transform-origin: left;
            transition: transform var(--transition-fast);
        }

        .btn-outline:hover {
            color: #000000;
        }
        
        .btn-outline:hover::before {
            transform: scaleX(1);
        }

        /* Navigation Bar */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: var(--navbar-height);
            background-color: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 1000;
            transition: height 0.3s ease, padding 0.3s ease, background-color 0.3s ease, backdrop-filter 0.3s ease;
            border-bottom: 1px solid rgba(212, 160, 23, 0.3);
        }

        .navbar.scrolled {
            height: 60px;
            background-color: rgba(0, 0, 0, 0.98);
            backdrop-filter: blur(10px);
        }

        .nav-logo img {
            height: 48px;
            width: auto;
            transition: height 0.3s ease;
        }

        .navbar.scrolled .nav-logo img {
            height: 38px;
        }

        .nav-links {
            display: flex;
            gap: 32px;
        }

        .nav-links a {
            font-size: 15px;
            font-weight: 500;
            color: var(--color-text-muted);
            transition: color 200ms ease;
            position: relative;
        }

        .nav-links a:hover,
        .nav-links a.active {
            color: var(--color-gold);
        }

        .nav-actions {
            display: flex;
            align-items: center;
        }

        .btn-call {
            padding: 10px 24px;
            font-size: 14px;
        }

        .menu-toggle {
            display: none;
            flex-direction: column;
            justify-content: space-between;
            width: 24px;
            height: 18px;
            cursor: pointer;
            z-index: 1001;
        }

        .menu-toggle span {
            display: block;
            height: 2px;
            width: 100%;
            background-color: var(--color-gold);
            transition: var(--transition-fast);
        }

        /* Mobile Navbar */
        @media (max-width: 1024px) {
            .navbar {
                padding: 0 20px;
                height: 60px;
            }
            .nav-logo img {
                height: 38px;
            }
            .nav-actions .btn-call {
                display: none;
            }
            .menu-toggle {
                display: flex;
            }
            .nav-links {
                position: fixed;
                top: 0;
                right: -100%;
                width: 100%;
                height: 100vh;
                background-color: rgba(10, 10, 10, 0.98);
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: transform 0.3s ease;
                gap: 0;
            }
            .nav-links.open {
                transform: translateX(-100%);
            }
            .nav-links li {
                width: 100%;
                text-align: center;
            }
            .nav-links a {
                display: block;
                padding: 20px;
                font-size: 18px;
                color: var(--color-white);
            }
            .nav-links a.active {
                color: var(--color-gold);
            }
            .mobile-call {
                display: block !important;
                margin-top: 20px;
            }
        }
        .mobile-call {
            display: none;
        }

        /* Footer */
        .footer {
            border-top: 1px solid var(--color-gold);
            background-color: var(--color-black-card);
            padding: 60px 20px 40px;
            text-align: center;
        }

        .footer-logo {
            font-family: var(--font-heading);
            font-size: 32px;
            font-weight: 700;
            color: var(--color-gold);
            margin-bottom: 8px;
        }

        .footer-tagline {
            font-family: var(--font-heading);
            font-size: 18px;
            color: var(--color-white);
            margin-bottom: 32px;
            font-style: italic;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }

        .footer-links a {
            color: var(--color-white);
            text-decoration: none;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: color 0.2s ease;
        }

        .footer-links a:hover {
            color: var(--color-gold);
        }

        .footer-social {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-bottom: 32px;
        }

        .footer-social a {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            color: rgba(255, 255, 255, 0.4);
            font-size: 18px;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .footer-social a:hover {
            background: var(--color-gold);
            color: var(--color-background);
        }

        .footer-copyright {
            font-size: 13px;
            color: rgba(255, 255, 255, 0.3);
        }
    
    /* Blog Article Styles */
    .blog-article {
        max-width: 800px;
        margin: 120px auto 80px;
        padding: 0 20px;
    }
    .blog-breadcrumb {
        font-size: 14px;
        color: var(--color-gold);
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }
    .blog-breadcrumb a {
        color: var(--color-text-muted);
        text-decoration: none;
    }
    .blog-breadcrumb a:hover {
        color: var(--color-white);
    }
    .blog-header h1 {
        font-size: 42px;
        color: var(--color-white);
        margin-bottom: 16px;
        line-height: 1.25;
        word-wrap: break-word;
    }
    @media (max-width: 767px) {
        .blog-header h1 { font-size: 32px; }
    }
    .blog-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        font-size: 14px;
        color: var(--color-text-muted);
        margin-bottom: 32px;
        align-items: center;
    }
    .blog-meta i {
        color: var(--color-gold);
        margin-right: 6px;
    }
    .blog-hero-img {
        width: 100%;
        height: 400px;
        object-fit: cover;
        border-radius: var(--border-radius);
        margin-bottom: 40px;
    }
    @media (max-width: 767px) {
        .blog-hero-img { height: 250px; margin-bottom: 24px;}
    }
    .blog-content {
        font-size: 17px;
        line-height: 1.8;
        color: #E0E0E0;
    }
    @media (max-width: 767px) {
        .blog-content { font-size: 16px; }
    }
    .blog-content h2 {
        font-size: 28px;
        color: var(--color-gold);
        margin: 40px 0 20px;
        line-height: 1.3;
    }
    @media (max-width: 767px) {
        .blog-content h2 { font-size: 24px; margin: 30px 0 16px; }
    }
    .blog-content p {
        margin-bottom: 24px;
    }
    .blog-content ul {
        margin-bottom: 24px;
        padding-left: 20px;
    }
    .blog-content li {
        margin-bottom: 10px;
        list-style-type: disc;
    }
    .blog-share {
        margin-top: 60px;
        padding-top: 30px;
        border-top: 1px solid rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .blog-share span {
        font-weight: 600;
        color: var(--color-white);
    }
    .blog-share-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: rgba(212, 160, 23, 0.1);
        color: var(--color-gold);
        border: 1px solid rgba(212, 160, 23, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .blog-share-btn:hover {
        background: var(--color-gold);
        color: var(--color-black);
    }

    /* Related Articles */
    .related-articles {
        margin-top: 60px;
        padding-top: 40px;
        border-top: 1px solid rgba(212, 160, 23, 0.2);
    }
    .related-articles h3 {
        font-size: 24px;
        color: var(--color-white);
        margin-bottom: 24px;
    }
    .related-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
    }
    @media (max-width: 767px) {
        .related-grid { grid-template-columns: 1fr; }
    }
    .related-card {
        background: var(--color-black-card);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: var(--border-radius);
        overflow: hidden;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .related-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 160, 23, 0.3);
    }
    .related-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
    }
    .related-content {
        padding: 16px;
    }
    .related-title {
        font-size: 16px;
        color: var(--color-white);
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .related-link {
        font-size: 14px;
        color: var(--color-gold);
        font-weight: 600;
    }

    </style>
    
</head>
<body>
<nav class="navbar" id="navbar">
        <a href="index.html#home" class="nav-logo">
            <img src="logo.jpeg" alt="Royal Mandi Logo" style="max-height: 48px; width: auto; border-radius: 4px;">
        </a>
        
        <ul class="nav-links" id="nav-links">
            <li><a href="index.html#home">Home</a></li>
            <li><a href="index.html#about">About</a></li>
            <li><a href="index.html#menu">Menu</a></li>
            <li><a href="index.html#gallery">Gallery</a></li>
            <li><a href="index.html#reviews">Reviews</a></li>
            <li><a href="index.html#blog" class="active">Blog</a></li>
            <li><a href="index.html#contact">Contact</a></li>
            <li class="mobile-call">
                <a href="tel:+917795416101" class="btn btn-primary btn-call">Call Now</a>
            </li>
        </ul>
        
        <div class="nav-actions">
            <a href="tel:+917795416101" class="btn btn-outline btn-call">Call Now</a>
        </div>
        
        <div class="menu-toggle" id="mobile-menu" aria-label="Open menu">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </div>
    </nav>

    <main class="blog-article">
        <div class="blog-breadcrumb">
            <a href="index.html">Home</a> <i class="fas fa-chevron-right" style="font-size:10px;"></i> 
            <a href="index.html#blog">Blog</a> <i class="fas fa-chevron-right" style="font-size:10px;"></i> 
            <span style="color: var(--color-white);">{title}</span>
        </div>
        
        <header class="blog-header">
            <h1>{title}</h1>
            <div class="blog-meta">
                <span style="color: var(--color-gold); font-weight:600;">{category}</span>
                <span><i class="far fa-calendar-alt"></i> {date}</span>
                <span><i class="far fa-clock"></i> 4 Min Read</span>
            </div>
        </header>
        
        <img src="{image}" alt="{title}" class="blog-hero-img">
        
        <div class="blog-content">
            {content}
            
            <div class="blog-share">
                <span>Share this article:</span>
                <a href="https://api.whatsapp.com/send?text={title} - https://royalmandihouse.in/{filename}" target="_blank" class="blog-share-btn" aria-label="Share on WhatsApp"><i class="fab fa-whatsapp" style="font-size:20px;"></i></a>
                <button class="blog-share-btn" aria-label="Copy Link" onclick="navigator.clipboard.writeText('https://royalmandihouse.in/{filename}'); alert('Link copied to clipboard!');"><i class="fas fa-link"></i></button>
            </div>
        </div>

        <div class="related-articles">
            <h3>Read Next</h3>
            <div class="related-grid">
                {related}
            </div>
        </div>

    </main>
    
<footer class="footer">
        <div class="footer-content animate-on-scroll">
            <div class="footer-logo">ROYAL MANDI</div>
            <div class="footer-tagline">Dine Like Royalty</div>
            <div class="footer-links">
                <a href="index.html#home">Home</a>
                <a href="index.html#menu">Menu</a>
                <a href="index.html#gallery">Gallery</a>
                <a href="index.html#reviews">Reviews</a>
                <a href="index.html#blog">Blog</a>
                <a href="index.html#contact">Contact</a>
            </div>
            <div class="footer-social">
                <a href="https://instagram.com" target="_blank" aria-label="Visit our Instagram"><i class="fab fa-instagram"></i></a>
                <a href="https://facebook.com" target="_blank" aria-label="Visit our Facebook"><i class="fab fa-facebook-f"></i></a>
            </div>
            <div class="footer-copyright">
                &copy; 2026 Royal Mandi House. All Rights Reserved.
            </div>
        </div>
    </footer>
<!-- Scripts -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const mobileMenu = document.getElementById('mobile-menu');
            const navLinks = document.getElementById('nav-links');
            const navLinksItems = navLinks.querySelectorAll('a');
            
            mobileMenu.addEventListener('click', () => {
                navLinks.classList.toggle('open');
                const bars = mobileMenu.querySelectorAll('.bar');
                if (navLinks.classList.contains('open')) {
                    bars[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
                    bars[1].style.opacity = '0';
                    bars[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
                } else {
                    bars[0].style.transform = 'none';
                    bars[1].style.opacity = '1';
                    bars[2].style.transform = 'none';
                }
            });

            navLinksItems.forEach(link => {
                link.addEventListener('click', () => {
                    if (navLinks.classList.contains('open')) {
                        mobileMenu.click();
                    }
                });
            });

            const navbar = document.getElementById('navbar');
            window.addEventListener('scroll', () => {
                if (window.scrollY > 80) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }, { passive: true });
        });
    </script>
</body>
</html>
"""

blogs = [
    {
        "filename": "blog-1.html",
        "title": "What Makes Arabian Mandi So Popular?",
        "category": "ARABIAN FOOD",
        "date": "June 10, 2026",
        "image": "https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg",
        "excerpt": "Discover why Arabian Mandi has become one of the most loved dishes among food enthusiasts in Mangalore.",
        "seo_title": "What Makes Arabian Mandi So Popular? | Royal Mandi House",
        "meta_desc": "Explore the rich history, aromatic spices, and traditional cooking methods that make Arabian Mandi a favorite dish in Mangalore at Royal Mandi House.",
        "keywords": "Mandi in Mangalore, Arabian Mandi, Arabian food in Mangalore, Royal Mandi House",
        "content": """
<p>In the vibrant coastal city of Mangalore, where seafood and fiery curries have long dominated the culinary landscape, a new sensation has captured the hearts—and stomachs—of food enthusiasts. That sensation is Arabian Mandi. But what exactly makes this Middle Eastern import so irresistibly popular? At Royal Mandi House, we believe the magic lies in a perfect storm of history, technique, and exquisite Arabian food flavors.</p>

<h2>The Royal Origins of Mandi</h2>
<p>To truly understand Mandi's popularity, we must look to its roots. Originating from Hadhramaut, Yemen, the word "Mandi" is derived from the Arabic word <em>nada</em>, which translates to "dew." This perfectly describes the dewy, tender, and incredibly moist texture of the meat that sits atop the rice. Historically, nomadic Arabian tribes prepared Mandi for large gatherings, celebrations, and royal feasts. This communal aspect of dining—sharing a massive, aromatic platter of rice and meat—is something that resonates deeply with the family-oriented culture here in Mangalore.</p>

<h2>The Traditional Cooking Technique</h2>
<p>Unlike regular biryanis or pulaos, authentic Mandi relies on a unique cooking method that sets it apart from any other rice dish. Traditionally, it is cooked in a <em>taboon</em>—a special oven dug into the ground. Wood or charcoal burns intensely at the bottom, while the seasoned meat is suspended on a rack above a large pot of basmati rice.</p>
<p>As the meat slow-cooks over several hours, its rich, spiced juices drip directly into the rice below. At the same time, the smoke from the charcoal infuses the entire dish with a subtle, earthy smokiness. It is this slow, deliberate process that ensures every single grain of rice is packed with flavor, and the meat becomes so tender it practically melts off the bone.</p>

<h2>A Symphony of Aromatic Spices</h2>
<p>While South Indian cuisine is known for its intense heat, Arabian food in Mangalore offers a different kind of sensory experience. Mandi is characterized by its use of <em>Hawaij</em>, a traditional Yemeni spice blend. This aromatic mixture typically includes cardamom, cloves, black pepper, cumin, and saffron or turmeric. The spices are robust yet incredibly balanced, ensuring that the food is deeply flavorful without being overwhelmingly spicy. This makes Mandi an excellent choice for diners of all ages.</p>

<h2>The Ultimate Comfort Food</h2>
<p>There is a unique comfort in eating Mandi. The fragrant, long-grain basmati rice, paired with succulent pieces of chicken or mutton, creates a deeply satisfying meal. Whether you prefer the classic Al-Faham Mandi, with its perfectly grilled, smoky chicken, or the tender slow-cooked Mutton Mandi, the dish provides a wholesome, fulfilling dining experience.</p>
<p>Moreover, the tradition of serving Mandi on a large communal plate encourages connection. In today's fast-paced world, sitting down with friends and family to share a single, majestic platter of food brings people closer together, making the meal not just about sustenance, but about shared joy.</p>

<h2>Experience Authentic Mandi at Royal Mandi House</h2>
<p>The skyrocketing popularity of Mandi in Mangalore is a testament to the city's evolving palate and appreciation for authentic, global flavors. If you are searching for the most authentic Mandi experience in the city, look no further.</p>
<p>At <strong>Royal Mandi House</strong>, located in the heart of Hampankatta, we pride ourselves on bringing the true taste of Arabia to your table. Our chefs meticulously follow traditional slow-cooking methods to ensure every plate we serve is nothing short of royal.</p>
<br>
<h3>Ready to Taste the Magic?</h3>
<p>Gather your family and friends and join us for a feast you won't forget.</p>
<p><a href="index.html#menu" class="btn btn-primary" style="margin-top: 10px;">Explore Our Menu</a></p>
        """
    },
    {
        "filename": "blog-2.html",
        "title": "Al-Faham vs Broasted Chicken – What's the Difference?",
        "category": "KNOW YOUR FOOD",
        "date": "June 11, 2026",
        "image": "blog2.png",
        "excerpt": "Both are delicious, but they are worlds apart in preparation. Learn the difference between smoky Al-Faham and crispy Broasted chicken.",
        "seo_title": "Al-Faham vs Broasted Chicken: Difference Explained | Royal Mandi",
        "meta_desc": "Wondering about the difference between Al-Faham and Broasted Chicken? Learn how these two popular dishes are prepared at Royal Mandi House in Mangalore.",
        "keywords": "Al-Faham in Mangalore, Broasted Chicken, Arabian food, Royal Mandi House, Chicken recipes",
        "content": """
<p>When you sit down at a premier Arabian restaurant like Royal Mandi House, you are immediately faced with a delightful dilemma: what type of chicken should you order? Two of the undisputed heavyweights on our menu are Al-Faham and Broasted Chicken. While both are incredibly popular choices for food lovers in Mangalore, they offer entirely different culinary experiences.</p>

<h2>What is Al-Faham?</h2>
<p>If you love smoky, robust flavors, Al-Faham is the dish for you. Originating from the Middle East, Al-Faham translates to "charcoal" in Arabic, which perfectly describes its cooking method. </p>
<p>The preparation of authentic Al-Faham involves marinating a butterflied chicken in a rich, vibrant blend of Arabian spices. This marinade typically features a mix of garlic, ginger, coriander, cumin, paprika, and a touch of yogurt or olive oil to tenderize the meat. The true magic happens on the grill. The marinated chicken is cooked over open charcoal flames, allowing the fat to render slowly. This process locks in the juices while imparting an intense, earthy smokiness to the meat. The result is a beautifully charred exterior that gives way to succulent, heavily spiced chicken inside.</p>
<p><strong>Best paired with:</strong> Al-Faham is traditionally served alongside perfectly seasoned Mandi rice, soft Kubbus (pita bread), and a side of fresh garlic paste (Toum) to cool down the spices.</p>

<h2>What is Broasted Chicken?</h2>
<p>On the opposite end of the spectrum is Broasted Chicken, the ultimate comfort food for those who crave a satisfying crunch. The term "broasting" refers to a specific cooking technique that combines the principles of deep frying and pressure cooking.</p>
<p>To create the perfect Broasted Chicken, the meat is first marinated in a seasoned brine, ensuring that flavor penetrates deep into the bone. It is then coated in a seasoned flour mixture before being placed into a specialized pressure fryer. The pressure seals the exterior of the chicken instantly, preventing the cooking oil from seeping into the meat. The result? An incredibly crispy, golden-brown crust on the outside, and incredibly juicy, steaming-hot chicken on the inside.</p>
<p><strong>Best paired with:</strong> Broasted chicken is universally loved alongside crispy French fries, fresh coleslaw, and a generous serving of garlic dip.</p>

<h2>The Verdict: Which Should You Choose?</h2>
<p>Choosing between Al-Faham and Broasted Chicken ultimately comes down to your personal craving for the day.</p>
<ul>
    <li><strong>Choose Al-Faham if:</strong> You are in the mood for traditional Arabian food. The deep, smoky flavors and charcoal-grilled texture make it the perfect accompaniment to Mandi rice. It is a slightly healthier option since it is grilled rather than fried.</li>
    <li><strong>Choose Broasted Chicken if:</strong> You want an irresistible crunch. The combination of crispy skin and juicy meat makes it a fantastic, satisfying meal, especially when ordered as a combo with fries and a soft drink.</li>
</ul>

<h2>Taste the Best of Both Worlds</h2>
<p>At <strong>Royal Mandi House</strong>, we refuse to make you choose. Our expert chefs have perfected both techniques, ensuring that whether you order our signature Al-Faham Mandi or our Family Broasted Meal Combo, you are getting the absolute best in Mangalore.</p>
<br>
<h3>Craving a Feast?</h3>
<p>Why not try both? Visit us today or call to place your order.</p>
<p><a href="tel:+917795416101" class="btn btn-primary" style="margin-top: 10px;">Call Now to Order</a></p>
        """
    },
    {
        "filename": "blog-3.html",
        "title": "Why Mangalore is Falling in Love with Arabic Food",
        "category": "FOOD CULTURE",
        "date": "June 12, 2026",
        "image": "https://images.pexels.com/photos/12737656/pexels-photo-12737656.jpeg",
        "excerpt": "From coastal seafood to Arabian spices — discover how Mangalore’s food scene is embracing the bold flavors of Arabic cuisine.",
        "seo_title": "Why Mangalore is Falling in Love with Arabic Food | Royal Mandi",
        "meta_desc": "Discover the rise of Arabian food in Mangalore. See how local foodies are embracing Mandi, Al-Faham, and Kunafa at restaurants like Royal Mandi House.",
        "keywords": "Arabian food in Mangalore, Mandi in Mangalore, Mangalore food culture, Royal Mandi House",
        "content": """
<p>Mangalore has always been a city celebrated for its bold culinary heritage. Famous globally for its fiery fish curries, crispy Neer Dosa, and rich Ghee Roast, the coastal city boasts a palate that demands flavor. Yet, over the last few years, a fascinating shift has occurred. A quiet revolution has taken over the streets of Hampankatta, Balmatta, and beyond: Mangalore has wholeheartedly fallen in love with Arabian food.</p>

<h2>A Culinary Bridge Across the Arabian Sea</h2>
<p>The connection between the Malabar coast and the Middle East spans centuries, driven by ancient spice trades and modern-day expatriates. Many families in Mangalore have relatives working in the Gulf, meaning the flavors of Dubai, Oman, and Saudi Arabia have been slowly making their way into local households for decades. It was only a matter of time before these authentic flavors became a staple of the city's dining out culture.</p>

<h2>A Welcome Change of Pace</h2>
<p>While Mangalorean cuisine is undeniably delicious, it is often heavy on fiery chilies, tamarind, and coconut. Arabian food offers a brilliant contrast. Dishes like Mandi and Al-Faham rely on a more subtle, aromatic spice profile. Ingredients like saffron, cardamom, dried lime, and sumac create complex layers of flavor without the intense heat.</p>
<p>This subtlety appeals to a wide demographic. Whether it is a family dining with young children or foodies looking for a soothing yet flavorful meal, Arabian food provides the perfect, universally appealing option. The emphasis on high-quality, slow-cooked meats and fragrant basmati rice ensures that every meal is deeply comforting.</p>

<h2>The Power of Communal Dining</h2>
<p>One of the most significant reasons Arabian food has thrived in Mangalore is the culture of communal dining. In Arabian tradition, food is meant to be shared. A massive platter of Mandi placed in the center of the table invites everyone to dig in together.</p>
<p>At <strong>Royal Mandi House</strong>, we see this magic happen every day. Families, groups of college students, and colleagues gather around our tables, breaking bread (or in this case, sharing rice) in a way that fosters connection and joy. In a fast-paced world, sitting down to share a grand Arabian feast feels like a much-needed pause.</p>

<h2>The Best Arabian Food in Mangalore</h2>
<p>As the demand for Middle Eastern cuisine grows, so does the standard for authenticity. Mangaloreans are discerning food lovers; they know the difference between a hastily prepared dish and an authentic recipe.</p>
<p>That is why <strong>Royal Mandi House</strong> has quickly become a landmark for Arabian food in Mangalore. We don't cut corners. From importing the right spices to using traditional cooking techniques for our signature Al-Faham, Broasted Chicken, and unlimited Mandi rice, we are dedicated to providing an unparalleled dining experience.</p>
<br>
<h3>Join the Culinary Revolution</h3>
<p>If you haven't yet experienced the rich, smoky flavors of authentic Arabian cuisine, you are missing out on Mangalore's most exciting food trend.</p>
<p><a href="index.html#contact" class="btn btn-primary" style="margin-top: 10px;">Visit Royal Mandi House Today</a></p>
        """
    },
    {
        "filename": "blog-4.html",
        "title": "What is Kunafa? The Dessert Everyone Loves",
        "category": "DESSERTS",
        "date": "June 13, 2026",
        "image": "https://images.pexels.com/photos/115740/pexels-photo-115740.jpeg",
        "excerpt": "Unveil the sweet, cheesy, and crunchy magic of Kunafa, the traditional Middle Eastern dessert that is taking the culinary world by storm.",
        "seo_title": "What is Kunafa? The Ultimate Arabian Dessert | Royal Mandi House",
        "meta_desc": "Learn all about Kunafa, the traditional Middle Eastern dessert made with spun pastry and cheese, available at Royal Mandi House in Mangalore.",
        "keywords": "Kunafa in Mangalore, Arabian dessert, Kunafa recipe, Royal Mandi House, sweet treats",
        "content": """
<p>No grand Arabian feast is complete without a grand finale. While the smoky flavors of Al-Faham and the aromatic richness of Mandi are enough to satisfy any craving, there is always room for dessert. Enter Kunafa—a traditional Middle Eastern sweet treat that has taken the internet, and Mangalore, by storm.</p>

<h2>The Anatomy of a Perfect Kunafa</h2>
<p>If you have never experienced Kunafa, you are in for a treat. At its core, Kunafa (also spelled Knafeh or Kanafeh) is an incredible study in contrasts. It balances crunchy and gooey, sweet and savory, hot and cold. </p>
<p>The foundation of the dessert is a layer of <em>kataifi</em>, which is finely spun, shredded phyllo dough that looks almost like vermicelli noodles. This pastry is generously coated in melted butter or ghee, which ensures it bakes to a spectacular, golden-brown crispness. </p>
<p>Beneath this crunchy exterior lies a thick, decadent layer of mildly savory, stretchy cheese or rich clotted cream. Once baked to perfection, the entire dessert is drenched in a fragrant simple syrup, often infused with rose water or orange blossom water, and garnished with crushed pistachios.</p>

<h2>A Dessert Steeped in History</h2>
<p>Kunafa boasts a rich history that dates back centuries. Its exact origins are heavily debated among culinary historians, with countries across the Levant—including Palestine, Lebanon, and Jordan—all claiming it as their own. Legend has it that the dish was created for the Caliphs of the Umayyad Empire during the holy month of Ramadan to keep them full and energized during their fasting hours.</p>
<p>Regardless of where it originated, Kunafa has become a symbol of celebration, hospitality, and joy across the Middle East. Today, it is enjoyed worldwide, from the bustling streets of Istanbul to right here in Mangalore.</p>

<h2>Why Everyone is Obsessed</h2>
<p>What makes Kunafa so irresistible? It is the theatrical cheese pull, the satisfying crunch of the kataifi pastry, and the delicate floral notes of the syrup. Unlike overly sweet western desserts, the mildness of the cheese perfectly cuts through the sugar, ensuring that every bite is balanced and addictive.</p>

<h2>Experience the Best Kunafa in Mangalore</h2>
<p>At <strong>Royal Mandi House</strong>, we know that an authentic Arabian meal deserves an equally authentic dessert. That is why our chefs carefully prepare our Kunafa fresh, ensuring it arrives at your table piping hot, with the perfect golden crust and an unforgettable cheese pull.</p>
<p>Whether you choose our Classic Cream Kunafa or the rich Cream Cheese Kunafa, it is the ultimate way to cap off your dining experience.</p>
<br>
<h3>Save Room for Dessert!</h3>
<p>Next time you dine with us, make sure to order our signature Kunafa. Your sweet tooth will thank you.</p>
<p><a href="index.html#menu" class="btn btn-primary" style="margin-top: 10px;">View Our Dessert Menu</a></p>
        """
    }
]

# Generate related articles blocks
for i, blog in enumerate(blogs):
    related_html = ""
    for j, related in enumerate(blogs):
        if i == j: continue
        if len(related_html.split("related-card")) > 2: break # Only take 2 related
        related_html += f"""
                <a href="{related['filename']}" class="related-card">
                    <img src="{related['image']}" alt="{related['title']}" class="related-img">
                    <div class="related-content">
                        <div class="related-title">{related['title']}</div>
                        <div class="related-link">Read More &rarr;</div>
                    </div>
                </a>"""
    
    html = blog_template.replace('{filename}', blog["filename"])
    html = html.replace('{title}', blog["title"])
    html = html.replace('{category}', blog["category"])
    html = html.replace('{date}', blog["date"])
    html = html.replace('{image}', blog["image"])
    html = html.replace('{seo_title}', blog["seo_title"])
    html = html.replace('{meta_desc}', blog["meta_desc"])
    html = html.replace('{keywords}', blog["keywords"])
    html = html.replace('{content}', blog["content"])
    html = html.replace('{og_title}', blog["title"])
    html = html.replace('{related}', related_html)
    
    with open(blog["filename"], "w", encoding="utf-8") as f:
        f.write(html)

print("Generated 4 blog HTML files.")

# Now update index.html blog section and mobile css
with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# Update the blog grid
new_blog_grid = '<div class="blog-grid">\n'
for blog in blogs:
    new_blog_grid += f"""            <a href="{blog['filename']}" class="blog-card animate-on-scroll">
                <div class="blog-card-img-wrapper">
                    <img class="blog-card-img" src="{blog['image']}" alt="{blog['title']}" loading="lazy">
                </div>
                <div class="blog-card-body">
                    <div class="blog-tag">{blog['category']}</div>
                    <h3 class="blog-title">{blog['title']}</h3>
                    <p class="blog-excerpt">{blog['excerpt']}</p>
                    <span class="blog-read-more">Read More <i class="fas fa-arrow-right"></i></span>
                </div>
            </a>\n"""
new_blog_grid += '        </div>'

# Regex replace the blog grid in index.html
pattern = re.compile(r'<div class="blog-grid">.*?</div>\s*</section>', re.DOTALL)
replacement = new_blog_grid + '\n    </section>'
index_content = pattern.sub(replacement, index_content, count=1)

# Add some global mobile CSS fixes if they aren't already there (they mostly are, but ensuring body doesn't overflow)
if 'max-width: 100vw;' not in index_content:
    index_content = index_content.replace('overflow-x: hidden;', 'overflow-x: hidden;\n            max-width: 100vw;')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_content)

print("Updated index.html.")
