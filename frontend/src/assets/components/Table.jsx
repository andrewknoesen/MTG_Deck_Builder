import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';

export default function BasicTable({ rows, handleQtyChange }) {

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

  return (
    <TableContainer sx={{ height: '90vh', width: '30vw' }} component={Paper}>
      <Table
        aria-labelledby="tableTitle"
        size={'small'}
        stickyHeader
      >
        <TableHead>
          <TableRow
            sx={{ border: 3 }}>
            <TableCell>Card</TableCell>
            <TableCell align="right">Qty</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="right">
                <TextField
                  type="number"
                  value={row.qty}
                  onChange={(e) => handleQtyChange(row.name, e.target.value)}
                  onBlur={(e) => handleBlur(row.name, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(e, row.name, e.target.value)}
                  variant="standard"
                  inputProps={{ min: 0 }}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
