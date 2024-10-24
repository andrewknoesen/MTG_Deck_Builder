import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import { useState, useEffect, useCallback } from 'react'
import { CircularProgress } from '@mui/material';
import axios from 'axios';


export default function EnhancedTable({ rows, handleQtyChange }) {

  const [cardImage, setCardImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleBlur = (name, qty) => {
    // Set qty to 0 if the field is empty
    if (qty === '') {
      handleQtyChange(name, 0);
    } else {
      handleQtyChange(name, Number(qty))
    }
  };

  const handleKeyDown = (e, name, qty) => {
    // Set qty to 0 if Enter is pressed and field is empty
    if (e.key === 'Enter') {
      handleQtyChange(name, qty === '' ? 0 : qty);
    }
  };

  const fetchCardImage = async (cardName) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/get_card_image?query=${encodeURIComponent(cardName)}`);
      console.log({response})
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
        aria-labelledby="Order"
        size={'small'}
        stickyHeader
      >
        <TableHead>
          <TableRow
            sx={{ border: 3 }}>
            <TableCell><strong>Card</strong></TableCell>
            <TableCell align="center"><strong>Qty</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <Tooltip
                title={
                  isLoading ? (
                    <CircularProgress size={20} />
                  ) : cardImage ? (
                    <img src={cardImage} alt={`${row.name} card`} style={{ maxWidth: '200px' }} />
                  ) : (
                    "Image not available"
                  )
                }
                onOpen={() => handleMouseEnter(row.name)}
                onClose={handleMouseLeave}
              >
                <TableCell component="th" scope="row">
                  {row.name}
                </TableCell>
              </Tooltip>
              <TableCell align="center" style={{ width: '30%', whiteSpace: 'nowrap' }}>
                <TextField
                  type="number"
                  value={row.qty}
                  onChange={(e) => handleQtyChange(row.name, e.target.value)}
                  onBlur={(e) => handleBlur(row.name, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(e, row.name, e.target.value)}
                  // variant="standard"
                  inputProps={{ min: 0,  style: { textAlign: 'center' } }}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
