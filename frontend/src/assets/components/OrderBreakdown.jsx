import * as React from 'react';
import { Typography } from '@mui/material';

import SummaryTable from '../components/SummaryTable'


export default function OrderBreakdown({ report }) {
    return (
        <div style={{ flex: 1.5, alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'start' }}>
                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                    <strong>Order Breakdown</strong>
                </Typography>
            </div>
            <div style={{ alignItems: 'start' }}>
                <SummaryTable purchaseData={report} />
            </div>
        </div>
    )
}