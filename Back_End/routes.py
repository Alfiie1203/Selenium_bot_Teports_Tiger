import logging
from flask import Blueprint, jsonify, request, render_template
from Back_End.Example1 import example1
from Back_End.Example2 import example2
from Back_End.Example3 import example3
from Back_End.Example4 import example4
from Back_End.Example5 import example5

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint of the application
tiger_processes = Blueprint('tiger_processes', __name__)

# URL is fixed in the backend but passed to the template
URL = "https://tiger.vialto.com/#/my-favorites"
DEFAULT_DOWNLOAD_DIR = 'G:\\Shared drives\\ES Vialto Campañas de Renta\\LA - INPUT\\ANNUAL\\INPUT ALTERYX'

@tiger_processes.route('/')
def index():
    return render_template('index.html', url=URL, download_dir=DEFAULT_DOWNLOAD_DIR)

@tiger_processes.route('/bot/<bot_name>', methods=['POST'])
def ejecutar_bot_route(bot_name):
    try:
        # Get JSON data from the request body
        data = request.get_json()
        url = data.get('url')  # Now we accept the URL from the client
        user = data.get('user')
        password = data.get('pass')
        download_dir = data.get('download_dir')
        new_name = data.get('new_Name')

        # Ensure that all fields are provided
        if not user or not password or not download_dir or not url:
            return jsonify({"error": "Missing URL, user, password, or download directory"}), 400

        # Determines which bot function to run
        if bot_name == 'example1':
            example1.main(url, user, password, download_dir)
            return jsonify({"info": f"The bot {bot_name} was successfully executed"})
        elif bot_name == 'example2':
            
            example2.main(url, user, password, download_dir, new_name)
            return jsonify({"info": f"The bot {bot_name} was successfully executed"})
        elif bot_name == 'example3':
            example3.main(url, user, password, download_dir)
            return jsonify({"info": f"The bot {bot_name} was successfully executed"})
        elif bot_name == 'example4':
            
            example4.main(url, user, password, download_dir, new_name)
            return jsonify({"info": f"The bot {bot_name} was successfully executed"})
        elif bot_name == 'example5':
            example5.main(url, user, password, download_dir)
            return jsonify({"info": f"The bot {bot_name} was successfully executed"})
        else:
            # Case when the bot_name does not match any of the previous ones
            return jsonify({"error": f"The bot {bot_name} is not valid"}), 400

    except Exception as e:
        logger.error(f"Error trying to run the bot {bot_name}: {str(e)}")
        return jsonify({"error": f"Error running the bot {bot_name}"}), 500
