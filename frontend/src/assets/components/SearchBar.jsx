import * as React from 'react';
import { useState, useEffect, useCallback } from 'react'
import axios from 'axios';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import debounce from 'lodash/debounce';

export default function FreeSolo({ setText }) {
    const [options, setOptions] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchOptions = useCallback(async (query) => {
        if (query) {
            setLoading(true);
            setError(null);
            try {
                const response = await axios.get(`http://localhost:8000/get_card_autocomplete?query=${encodeURIComponent(query)}`, {
                    withCredentials: true
                });
                setOptions(response.data); // Adjust this based on your API response structure
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to fetch suggestions. Please try again.');
                setOptions([]);
            } finally {
                setLoading(false);
            }
        } else {
            setOptions([]);
        }
    }, []);

    // Create a debounced version of fetchOptions
    const debouncedFetchOptions = useCallback(
        debounce((query) => fetchOptions(query), 600),
        [fetchOptions]
    );

    useEffect(() => {
        debouncedFetchOptions(inputValue);
        // Cleanup function to cancel the debounce on unmount
        return () => debouncedFetchOptions.cancel();
    }, [inputValue, debouncedFetchOptions]);

    return (
        <Autocomplete
            autoSelect={true}
            autoHighlight={true}
            id="autoCompleteSearch"
            options={options}
            loading={loading}
            renderInput={(params) => (
                <TextField
                    {...params}
                    variant="standard"
                    label="Search card"
                />
            )}
            onInputChange={(event, newInputValue) => {
                setInputValue(newInputValue);
                setText(newInputValue);
            }}
        />
    );
}