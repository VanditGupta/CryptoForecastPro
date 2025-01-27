import React from "react";
import { Pie } from "react-chartjs-2";
import redditData from "../data/redditData.json";

const SentimentChart = () => {
  const sentimentCounts = {
    Positive: redditData.filter((post) => post.Sentiment_Label === "Positive").length,
    Neutral: redditData.filter((post) => post.Sentiment_Label === "Neutral").length,
    Negative: redditData.filter((post) => post.Sentiment_Label === "Negative").length,
  };

  const data = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        data: Object.values(sentimentCounts),
        backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
      },
    ],
  };

  return (
    <div>
      <h2>Sentiment Distribution</h2>
      <Pie data={data} />
    </div>
  );
};

export default SentimentChart;
