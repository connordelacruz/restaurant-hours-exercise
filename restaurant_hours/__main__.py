from restaurant_hours import create_app

if __name__ == '__main__':
    app = create_app()
    # NOTE: My laptop was having issues with the default port of 5000, so using 8000
    app.run(port=8000, debug=True)
