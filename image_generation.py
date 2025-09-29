import pandas as pd
import requests
import time
def generate_image(prompt):
	"""
	Uses Hugging Face's free Stable Diffusion demo API to generate an image from a prompt.
	"""
	api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
	headers = {
		"Accept": "application/json",
		# "Authorization": ""
	}
	payload = {"inputs": prompt}
	try:
		response = requests.post(api_url, headers=headers, json=payload, timeout=60)
		if response.status_code == 200:
			result = response.json()
			if isinstance(result, dict) and "error" in result:
				return f"Error: {result['error']}"
			if isinstance(result, list) and len(result) > 0 and "generated_image" in result[0]:
				return result[0]["generated_image"]
			if "url" in result:
				return result["url"]
			return str(result)
		else:
			return f"API Error: {response.status_code}"
	except Exception as e:
		return f"Exception: {e}"

def main():
	input_excel = 'image_generation/test_image_generation .xlsx'
	prompt_column = 'Unnamed: 5'
	output_excel = 'image_generation/output.xlsx'

	df = pd.read_excel(input_excel)
	if prompt_column not in df.columns:
		print(f"Column '{prompt_column}' not found in the Excel file.")
		return

	images = []
	for prompt in df[prompt_column]:
		if pd.isna(prompt) or str(prompt).strip() == "":
			images.append("")
			continue
		print(f"Generating image for prompt: {prompt}")
		image_data = generate_image(prompt)
		images.append(image_data)
		time.sleep(2)  # Avoid rate limits

	df['Generated_Image'] = images
	df.to_excel(output_excel, index=False)
	print(f"Done! Output written to {output_excel}")

if __name__ == "__main__":
	main()
