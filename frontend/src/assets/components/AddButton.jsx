import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';

export default function IconButtons({ text, onAdd }) {
  return (
    <IconButton aria-label="add" size="large"  
    onClick={onAdd}>
      <AddIcon fontSize="inherit" />
    </IconButton>
  );
}
