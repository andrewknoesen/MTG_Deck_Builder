import { useState } from 'react';
import TextField from '@mui/material/TextField';

export default function QtyField({ setQty }) {
    const [value, setValue] = useState(1); // Default value is set to 1

    const handleChange = (event) => {
        const newValue = event.target.value;
        if (newValue !== ''){
        // Ensure value is not less than 0
        if ( newValue < 0) {
            setValue(0); // Set the input field value to 0
            setQty(0);   // Update the quantity to 0
        } else {
            setValue(Number(newValue)); // Update the input field value
            setQty(Number(newValue)); // Update the quantity
        }
    } else {
        setValue(newValue)
    }

    };

    return (
        <TextField
            id="standard-number"
            label="Qty"
            type="number"
            // defaultValue={1}
            value={value}
            variant="standard"
            onChange={handleChange}
        />
    );
}