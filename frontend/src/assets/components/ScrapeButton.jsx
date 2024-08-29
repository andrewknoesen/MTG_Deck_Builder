import * as React from 'react';
import Button from '@mui/material/Button';

export default function ScrapeButton({rows}){
    return(
        <Button
            variant="contained"
            onClick={() => alert(JSON.stringify(rows, null, 2))}> {/* Pretty-print JSON */}
            Build order
            </Button>
    )
}