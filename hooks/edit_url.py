def on_page_context(context, page, config, nav):
    base = "https://github.com/v3xctrl/wiki/edit/master/docs/"
    page.edit_url = base + page.file.src_path
    return context
