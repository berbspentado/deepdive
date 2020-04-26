from .app import app
import deepdive_web.views


if __name__ == '__main__':
    app.run(debug=True)