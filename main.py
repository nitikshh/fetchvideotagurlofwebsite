import os
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/videoUrl', methods=['GET'])
def get_video_url():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing."}), 400

    try:
        # Chrome options with headless mode and user profile settings
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (needed in headless mode)

        # Initialize Chrome WebDriver with Chrome options
        driver = webdriver.Chrome(options=chrome_options)

        # Load the webpage
        driver.get(url)

        try:
            # Wait until the video tag is present
            video_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            if video_tag:
                # Get the video src attribute
                video_src = video_tag.get_attribute('src')
                if not video_src:
                    # If no src attribute on video tag, check source tag inside video tag
                    source_tag = video_tag.find_element(By.TAG_NAME, "source")
                    video_src = source_tag.get_attribute('src') if source_tag else "Video source URL not found."
                return jsonify({"video_src": video_src})
            else:
                return jsonify({"error": "Video tag not found."}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred while waiting for the video tag: {str(e)}"}), 500
        finally:
            driver.quit()  # Always quit the driver to close the browser session
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
