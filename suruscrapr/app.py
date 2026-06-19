try:
    from . import create_app
except ImportError:
    from suruscrapr import create_app

from scraper import main

app = create_app()


if __name__ == '__main__':
    main.scheduledScrape()
    app.run(debug=True)