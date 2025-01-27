from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

# Load Reddit data
reddit_csv_path = "app/reddit_daily_data_all_cryptos.csv"
reddit_data = pd.read_csv(reddit_csv_path)

# Combine all text from the Combined_Text column for the word cloud
text = " ".join(reddit_data["Combined_Text"])

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# Save the word cloud image to the app folder
wordcloud_path = "app/wordcloud.png"
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Reddit Discussion Topics Word Cloud", fontsize=16)
plt.savefig(wordcloud_path)
# plt.show()
print(f"Word cloud saved as '{wordcloud_path}'")
