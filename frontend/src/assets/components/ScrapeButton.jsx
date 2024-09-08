import * as React from 'react';
import Button from '@mui/material/Button';
import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

export default function ScrapeButton({rows, setReport}){
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    
    const fetchOptions = useCallback(async (query) => {
        if (query) {
            setLoading(true);
            setError(null);
            try {
                const response = await axios.post(`http://localhost:8000/optimize_custom_order`, {"order": query}, {
                    withCredentials: true
                });
                setReport(response.data)
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to fetch suggestions. Please try again.');
            } finally {
                setLoading(false);
            }
        } else {
            setReport([])
        }
    }, []);

    return(
        <Button
            variant="contained"
            // onClick={() => alert(JSON.stringify(rows, null, 2))}> {/* Pretty-print JSON */}
            onClick={() => fetchOptions(rows)}> 
            Build order
            </Button>
    )
}