document.addEventListener('DOMContentLoaded', function () {
	const logoutLink = document.querySelector('a[href="/admin/logout/"]');
	if (logoutLink) {
		logoutLink.setAttribute('href', '/logout/');
	}
});
