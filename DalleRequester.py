#Not guaranteed to work for stf/NERF files or even for Shap-e, this is just a sample API Request for DALLE

from openai import OpenAI
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url