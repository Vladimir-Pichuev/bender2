def get_screen_resolution():
    from screeninfo import get_monitors
    monitor = get_monitors()[0]
    return monitor.width, monitor.height
