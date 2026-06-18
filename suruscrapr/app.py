try:
    from . import create_app
except ImportError:
    from suruscrapr import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)