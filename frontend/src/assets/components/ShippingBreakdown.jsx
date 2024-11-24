import * as React from 'react';
import { Typography } from '@mui/material';

export default function ShippingBreakdown({ report }) {
    return (
        <div style={{ alignItems: 'start' }}>
            <div style={{ display: 'flex', alignItems: 'start' }}>
                <Typography variant="h6" sx={{ color: 'black', padding: 1 }}>
                    <strong>Shipping Breakdown</strong>
                </Typography>
            </div>
            <div style={{ display: 'flex', alignItems: 'start' }}>
                <Typography variant="body1" sx={{ color: 'black', padding: 1 }}>
                    {report?.report?.shipping ? (
                        Object.entries(report.report.shipping).map(([key, value]) => (
                            <div style={{ display: 'flex', alignItems: 'start' }}>
                                <strong>{key}:&nbsp;</strong>  R{JSON.stringify(value)} <br /> {/* &nbsp; is being used to add a white space */}
                            </div>
                        ))
                    ) : (
                        "No shipping information available"
                    )}
                </Typography>
            </div>
        </div>
    )
}