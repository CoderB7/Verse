document.addEventListener('DOMContentLoaded', function () {
    const themeStyle = document.getElementById('theme-style');
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const currentThemeIcon = document.getElementById('currentThemeIcon');

    const lightIconSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>';
    const darkIconSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon-star"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/><path d="M20 3v4"/><path d="M22 5h-4"/></svg>';

    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            currentThemeIcon.innerHTML = darkIconSVG;
        } else {
            currentThemeIcon.innerHTML = lightIconSVG;
        }
    }

    // Check if dark mode is already enabled
    if (localStorage.getItem('theme') === 'dark') {
        themeStyle.href = darkThemeUrl;
        document.body.classList.replace('bg-light', 'bg-dark');
        document.body.classList.replace('text-dark', 'text-light');
        updateThemeIcon('dark');
    } else {
        themeStyle.href = lightThemeUrl;
        updateThemeIcon('light');
    }

    dropdownItems.forEach(item => {
        item.addEventListener('click', function () {
            const theme = this.getAttribute('data-theme');
            if (theme === 'dark') {
                themeStyle.href = darkThemeUrl;
                localStorage.setItem('theme', 'dark');
                document.body.classList.replace('bg-light', 'bg-dark');
                document.body.classList.replace('text-dark', 'text-light');
                updateThemeIcon('dark');
            } else {
                themeStyle.href = lightThemeUrl;
                localStorage.setItem('theme', 'light');
                document.body.classList.replace('bg-dark', 'bg-light');
                document.body.classList.replace('text-light', 'text-dark');
                updateThemeIcon('light');
            }
        });
    });
});
