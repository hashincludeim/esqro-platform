
// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
            
            // Close mobile menu if open
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
    
    // Simple form handling for CTAs (you can replace with actual form submission)
    const ctaButtons = document.querySelectorAll('.btn-primary');
    ctaButtons.forEach(button => {
        if (button.textContent.includes('Start Free Trial') || button.textContent.includes('Start Your Free Trial')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                // Replace this with your actual form handling or redirect
                alert('Free trial signup coming soon! Please contact us for early access.');
            });
        }
    });
    
    // Demo button handler
    const demoButton = document.querySelector('.btn-secondary');
    if (demoButton && demoButton.textContent.includes('Watch Demo')) {
        demoButton.addEventListener('click', function(e) {
            e.preventDefault();
            // Replace this with your actual demo video or modal
            alert('Demo video coming soon! Contact us to schedule a live demo.');
        });
    }
    
    // Contact sales button
    const contactButtons = document.querySelectorAll('button');
    contactButtons.forEach(button => {
        if (button.textContent.includes('Contact Sales')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                // Replace with actual contact form or mailto
                window.location.href = 'mailto:sales@esqro.com?subject=Enterprise Plan Inquiry';
            });
        }
    });
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe feature cards and pricing cards
    const animatedElements = document.querySelectorAll('.feature-card, .pricing-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Add some interactive hover effects
document.addEventListener('DOMContentLoaded', function() {
    // Add tilt effect to dashboard mockup
    const dashboardMockup = document.querySelector('.dashboard-mockup');
    if (dashboardMockup) {
        dashboardMockup.addEventListener('mouseenter', function() {
            this.style.transform = 'perspective(1000px) rotateY(-2deg) scale(1.02)';
        });
        
        dashboardMockup.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateY(-5deg) scale(1)';
        });
    }
    
    // Add counter animation to stats
    const statNumbers = document.querySelectorAll('.stat-number');
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;
                animateCounter(target, finalValue);
                statsObserver.unobserve(target);
            }
        });
    });
    
    statNumbers.forEach(stat => {
        statsObserver.observe(stat);
    });
    
    function animateCounter(element, finalValue) {
        const isNumber = finalValue.match(/\d+/);
        if (!isNumber) return;
        
        const numericValue = parseInt(isNumber[0]);
        const suffix = finalValue.replace(numericValue.toString(), '');
        let currentValue = 0;
        const increment = numericValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                element.textContent = finalValue;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue) + suffix;
            }
        }, 30);
    }
});