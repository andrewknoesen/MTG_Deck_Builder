import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(name, qty) {
  return { name, qty };
}

function updateData(name, qty, setRows) {
    setRows(prevRows => {
        const newRows = [...prevRows];
        const existingRow = newRows.find(row => row.name === name);
        if (existingRow) {
          existingRow.qty += qty;  // Increment qty if entry exists
        } else {
          newRows.push(createData(name, qty));  // Create new entry if it doesn't exist
        }
        return newRows;
      });
}

const initialRows = [
  createData('Frozen yoghurt', 159),
  createData('Ice cream sandwich', 237),
  createData('Eclair', 262),
  createData('1Cupcake', 305),
  createData('G2ingerbread', 356),
  createData('Fr3ozen yoghurt', 159),
  createData('Ice4 cream sandwich', 237),
  createData('Ecla5ir', 262),
  createData('Eclabvvnmjfdir', 262),
  createData('Cupcakqwerfdse', 305),
  createData('Gingerbredsfgrtewsad', 356),
];

export default function BasicTable({ onAdd }) {
  const [rows, setRows] = React.useState(initialRows);
  const handleAdd = (name) => {
    if (name) {
      updateData(name, 1, setRows);
    }
  };

  // Pass handleAdd to the parent component
  React.useEffect(() => {
    onAdd(handleAdd);
  }, [onAdd]);

  return (
    <TableContainer sx={{ height: '90vh', width: '25vw' }} component={Paper}>
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
              <TableCell align="right">{row.qty}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
