from django.utils.safestring import mark_safe

from wagtail import hooks


@hooks.register("insert_global_admin_js")
def get_global_admin_js():
    return mark_safe(
    """
    <script>
    window.addEventListener('DOMContentLoaded', function () {
        document.addEventListener('wagtail:images-upload', function(event) {
            // will stop title pre-fill on single file uploads
            // will set the multiple upload title to the filename (with extension)
            event.preventDefault();
        });
    });
    </script>
    """
    )
