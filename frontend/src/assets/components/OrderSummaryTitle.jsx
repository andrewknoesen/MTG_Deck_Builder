import * as React from 'react';
import { Typography } from '@mui/material';


export default function OrderSummaryTitle() {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <Typography variant="h3" sx={{ color: 'black', padding: 1 }}>
                Order Summary
            </Typography>
        </div>
    )
}