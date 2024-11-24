import * as React from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
import { useState, useCallback } from 'react';
import axios from 'axios';

export default function ScrapeButton({ rows, setReport }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchOptions = useCallback(async (query) => {
        if (query) {
            setLoading(true);
            setError(null);
            try {
                const response = await axios.post(
                    `http://localhost:8000/optimize_custom_order`,
                    { order: query },
                    {
                        withCredentials: true,
                    }
                );
                setReport(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to fetch suggestions. Please try again.');
            } finally {
                setLoading(false);
            }
        } else {
            setReport([]);
        }
    }, [setReport]);

    return (
        <LoadingButton
            variant="contained"
            onClick={() => fetchOptions(rows)}
            loading={loading}
            disabled={loading}
        >
            {loading ? 'Building order...' : 'Build order'}
        </LoadingButton>
    );
}