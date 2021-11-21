"""
Contains the methods that will need to be called by the front-end.
If arguments are passed in from the front-end in a dictionary, then they need to be decoded by calling arguments = request.get_json()
The '@app*' tags will need to be customized accordingly.
"""
import io
import json
import nftUtil
import base64

from flask import Flask, request, jsonify
from flask.helpers import make_response, send_file, send_from_directory
from flask_cors import CORS, cross_origin

# front-end folder name
# connect flask to front end
# do not need static_url_path
app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app)


@app.route("/images/<tokenId>", methods=["GET"])
def GetImage(tokenId):
    """
    This will retrieve the imageType and imageBinaryString from the database.
      1. Then you can display the imageBinaryString as a png file on a web page:
         https://newbedev.com/displaying-a-byte-array-as-an-image-using-javascript
         https://stackoverflow.com/questions/20756042/how-to-display-an-image-stored-as-byte-array-in-html-javascript
      2. Or you can turn the binary string into a PIL image:
           from PIL import Image
           image = Image.open(io.BytesIO(imageBinaryString))
           image.show()
      3. Or you can save it as an actual .png file:
           with open(str(tokenId) + '.' + imageType, 'wb') as f:
             f.write(imageBinaryString)
    """
    try:
        # Cannot return imageBinaryString or PIL.Image as json because you get an error: 'Object of type bytes is not JSON serializable'
        imageType, imageBinaryString = nftUtil.GetImage(tokenId)
        if imageType is None or imageBinaryString is None:
            return jsonify(None)

        # works
        # return send_file(io.BytesIO(imageBinaryString), mimetype='image/' + imageType, attachment_filename='%s.png' % tokenId)

        # option 2
        mimetype = "image/" + imageType
        attachment_filename = str(tokenId) + "." + imageType
        return send_file(io.BytesIO(imageBinaryString), mimetype=mimetype, attachment_filename=attachment_filename)

        # return jsonify({'imageType': imageType, 'imageBinaryString': imageBinaryString})
        # return imageType, imageBinaryString
    except:
        # A completely unexpected error (like unable to connect to the database) will return a stack trace in the errorMessage.
        # return json.dumps({'success':False, 'imageType':None, 'imageBinaryString': imageBinaryString, 'errorMessage':nftUtil.ProcessException()})
        return jsonify({"success": False, "errorMessage": nftUtil.ProcessException()})


@app.route("/metadata/<tokenIdJson>", methods=["GET"])
def GetMetadata(tokenIdJson):
    """
    Find the metadata associated with the input tokenIdJson.
      'tokenIdJson' : The sequential integer id (1, 2, 3, ...)
    """
    try:
        # this function can only return the metadata, nothing else.
        metadata = nftUtil.GetMetadata(tokenIdJson)
        return jsonify(metadata)
    except:
        # A completely unexpected error (like unable to connect to the database) will return a stack trace in the errorMessage.
        return jsonify({"success": False, "metadata": None, "errorMessage": nftUtil.ProcessException()})


@app.route("/setTokensMinted/<tokensMinted>", methods=["PUT"])
def SetTokensMinted(tokensMinted):
    try:
        nftUtil.SetTokensMinted(tokensMinted)
        return jsonify({"success": True, "tokensMinted": tokensMinted})
    except:
        return jsonify({"success": False})


@app.route("/setTotalTokens/<totalTokens>", methods=["PUT"])
def SetTotalTokens(totalTokens):
    try:
        nftUtil.SetTotalTokens(totalTokens)
        return jsonify({"success": True, "totalTokens": totalTokens})
    except:
        return jsonify({"success": False})


# generate html file on / route
@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run()
