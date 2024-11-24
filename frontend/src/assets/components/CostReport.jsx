import * as React from 'react';
import { Typography } from '@mui/material';

export default function CostReport({ report }) {
    return (
        <div style={{ alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'start' }}>
                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                    <strong>Total Cost</strong>
                </Typography>
            </div>
            <div style={{ display: 'flex', alignItems: 'start' }}>
                <Typography variant="body1" sx={{ color: 'black', padding: 1 }}>
                    {report?.report?.total ? (
                        <div style={{ display: 'flex', alignItems: 'start' }}>
                            <strong>Total:&nbsp;</strong> R{report?.report?.total}<br />
                        </div>
                    ) : (
                        "No costing data available"
                    )}
                </Typography>
            </div>
        </div>
    )
}