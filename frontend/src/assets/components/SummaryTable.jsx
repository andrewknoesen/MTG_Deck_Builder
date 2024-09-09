import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from '@mui/material';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import { useState, useEffect, useCallback } from 'react'
import { CircularProgress } from '@mui/material';
import axios from 'axios';


const flattenPurchaseData = (data) => {
  const flattened = [];
  Object.entries(data).forEach(([store, products]) => {
    Object.entries(products).forEach(([cardName, cardDetails]) => {
      Object.entries(cardDetails).forEach(([id, details]) => {
        flattened.push({
          store,
          cardName,
          id,
          ...details
        });
      });
    });
  });
  return flattened;
};

const PurchaseTable = ({ purchaseData }) => {
  const data = purchaseData?.report?.purchase || {};

  const flattenedData = flattenPurchaseData(data);

  const [cardImage, setCardImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCardImage = async (cardName) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/get_card_image?query=${encodeURIComponent(cardName)}`);
      console.log({ response })
      setCardImage(response.data.small);
    } catch (error) {
      console.error(`Error fetching image for ${cardName}:`, error);
      setCardImage(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMouseEnter = (cardName) => {
    fetchCardImage(cardName);
  };

  const handleMouseLeave = () => {
    setCardImage(null);
  };

  return (
    <TableContainer sx={{ height: '100%', width: '30vw' }} component={Paper}>
      <Table
        aria-labelledby="tableTitle"
        size={'small'}
        stickyHeader
      >
        <TableHead>
          <TableRow
            sx={{ border: 3 }}>
            <TableCell>Store</TableCell>
            <TableCell>Card Name</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Unit Price</TableCell>
            <TableCell>Gross</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {flattenedData.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.store}</TableCell>
              <Tooltip
                title={
                  isLoading ? (
                    <CircularProgress size={20} />
                  ) : cardImage ? (
                    <img src={cardImage} alt={`${row.cardName} card`} style={{ maxWidth: '200px' }} />
                  ) : (
                    "Image not available"
                  )
                }
                onOpen={() => handleMouseEnter(row.cardName)}
                onClose={handleMouseLeave}
              >
                <TableCell>{row.cardName}</TableCell>
              </Tooltip>
              <TableCell>{row.purchase_qty}</TableCell>
              <TableCell>{row.unit}</TableCell>
              <TableCell>{row.gross}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PurchaseTable;