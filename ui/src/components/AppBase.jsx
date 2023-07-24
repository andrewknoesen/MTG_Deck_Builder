import { useState } from 'react'

import Button from '@mui/material/Button';
import reactLogo from './../assets/react.svg'
import viteLogo from '/vite.svg'
import TopBar from './TopBar';
import SearchBar from './SearchBar';

import { ThemeProvider, createTheme } from '@mui/material/styles';

function AppBase({ title, children }) {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    const componentStyles = {
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'flex-start',
        top: '0',
        height: '100vh',
        width: '100vw',
        backgroundColor: 'blue',
    };

    


    return (

        <ThemeProvider theme={darkTheme}>
            <div>
                <TopBar title={title} />
            </div>
            <div style={componentStyles}>
                {children}
            </div>
        </ThemeProvider>
    )
}

export default AppBase
