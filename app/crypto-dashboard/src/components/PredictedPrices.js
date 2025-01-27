import React from "react";
import predictedPrices from "../data/predictedPrices.json";
import { Card, CardContent, Typography, Grid } from "@mui/material";

const PredictedPrices = () => {
  return (
    <div>
      <h2>Predicted Prices for Tomorrow</h2>
      <Grid container spacing={2}>
        {Object.entries(predictedPrices).map(([crypto, data]) => (
          <Grid item xs={6} sm={4} md={3} key={crypto}>
            <Card>
              <CardContent>
                <Typography variant="h6">{crypto}</Typography>
                <Typography variant="body1">Price: ${data.PredictedPrice}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default PredictedPrices;
