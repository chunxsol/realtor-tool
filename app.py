from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')


def generate_description(bedrooms, bathrooms, city, key_features):
	"""Generate a professional real estate listing description.

	bedrooms: int or str
	bathrooms: int/float or str
	city: str
	key_features: list or comma-separated string
	"""
	# Normalize bedrooms/bathrooms for display
	try:
		bedrooms_text = f"{int(bedrooms)}-bedroom"
	except Exception:
		bedrooms_text = f"{bedrooms}-bedroom" if bedrooms else "spacious"

	try:
		# Show integer baths without .0
		bths = float(bathrooms)
		if bths.is_integer():
			bathrooms_text = f"{int(bths)}-bathroom"
		else:
			bathrooms_text = f"{bths}-bathroom"
	except Exception:
		bathrooms_text = f"{bathrooms}-bathroom" if bathrooms else "well-appointed bathroom(s)"

	if isinstance(key_features, list):
		features_text = ', '.join(key_features)
	else:
		features_text = str(key_features).strip()

	if features_text:
		features_phrase = f"Notable features include {features_text}."
	else:
		features_phrase = ""

	description = (
		f"Discover an exceptional {bedrooms_text}, {bathrooms_text} residence in {city}. "
		f"Thoughtfully designed with modern finishes and attention to detail, this home offers comfort and refined living. "
		f"{features_phrase} Ideal for discerning buyers seeking convenience and style, the property blends tasteful aesthetics with practical living spaces. "
		f"Contact us to schedule a private showing and experience all this listing has to offer."
	)

	return description


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_route():
	data = request.get_json(force=True, silent=True) or {}
	bedrooms = data.get('bedrooms')
	bathrooms = data.get('bathrooms')
	city = data.get('city', 'this desirable area')
	key_features = data.get('key_features', '')

	description = generate_description(bedrooms, bathrooms, city, key_features)
	return jsonify({'description': description})


if __name__ == '__main__':
	app.run(debug=True)

