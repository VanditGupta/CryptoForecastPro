import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import todayCryptoData from "../data/todayCryptoData.json";

const CryptoTable = () => {
  const columns = [
    { field: "Date", headerName: "Date", width: 150 },
    { field: "Symbol", headerName: "Symbol", width: 100 },
    { field: "Open", headerName: "Open", width: 150 },
    { field: "High", headerName: "High", width: 150 },
    { field: "Low", headerName: "Low", width: 150 },
    { field: "Close", headerName: "Close", width: 150 },
  ];

  return (
    <div style={{ height: 400, width: "100%" }}>
      <h2>Today's Cryptocurrency Data</h2>
      <DataGrid rows={todayCryptoData} columns={columns} pageSize={5} />
    </div>
  );
};

export default CryptoTable;
