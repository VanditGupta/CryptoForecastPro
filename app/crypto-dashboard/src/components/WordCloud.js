import React, { useEffect, useRef } from "react";
import WordCloudLib from "wordcloud";
import redditData from "../data/redditData.json";

const WordCloud = () => {
  const canvasRef = useRef();

  useEffect(() => {
    const combinedText = redditData.map((post) => post.Combined_Text).join(" ");
    const wordFrequency = combinedText
      .split(" ")
      .reduce((freq, word) => {
        freq[word] = (freq[word] || 0) + 1;
        return freq;
      }, {});

    const wordArray = Object.entries(wordFrequency).map(([word, freq]) => [word, freq]);

    WordCloudLib(canvasRef.current, { list: wordArray, width: 800, height: 400 });
  }, []);

  return (
    <div>
      <h2>Word Cloud</h2>
      <canvas ref={canvasRef}></canvas>
    </div>
  );
};

export default WordCloud;
