import React from "react";
import { Container, Typography } from "@mui/material";
import CryptoTable from "./components/CryptoTable";
import PredictedPrices from "./components/PredictedPrices";
import SentimentChart from "./components/SentimentChart";
import WordCloud from "./components/WordCloud";

const App = () => {
  return (
    <Container>
      <Typography variant="h3" align="center" gutterBottom>
        Crypto Price Prediction Dashboard
      </Typography>
      <PredictedPrices />
      <CryptoTable />
      <SentimentChart />
      <WordCloud />
    </Container>
  );
};

export default App;
