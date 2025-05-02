import React, { useState } from 'react';
import { Box, FormControl, Select, MenuItem, Button, SelectChangeEvent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

interface Market {
    id: string;
    name: string;
    enabled: boolean;
}

const markets: Market[] = [
    { id: 'nova', name: 'Northern VA', enabled: true },
    { id: 'md', name: 'Maryland', enabled: false }
];

const HomePage: React.FC = () => {
    const [selectedMarket, setSelectedMarket] = useState<string>('');
    const navigate = useNavigate();

    const handleMarketChange = (event: SelectChangeEvent) => {
        setSelectedMarket(event.target.value);
    };

    const handleSearch = () => {
        if (selectedMarket === 'nova') {
            navigate('/listings');
        }
    };

    return (
        <Box sx={{ 
            minHeight: '100vh',
            width: '100vw',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            bgcolor: 'background.default'
        }}>
            <Typography 
                variant="h2" 
                component="h1" 
                sx={{ 
                    mb: 6,
                    fontWeight: 'bold',
                    color: 'primary.main'
                }}
            >
                House Hacker Calc
            </Typography>
            <Box sx={{ 
                display: 'flex',
                gap: 2,
                alignItems: 'center',
                maxWidth: '600px',
                width: '100%',
                px: 2
            }}>
                <FormControl fullWidth>
                    <Select
                        value={selectedMarket}
                        onChange={handleMarketChange}
                        displayEmpty
                        sx={{ 
                            bgcolor: 'background.paper',
                            '& .MuiSelect-select': {
                                py: 1.5
                            }
                        }}
                    >
                        <MenuItem value="" disabled>
                            Select a market
                        </MenuItem>
                        {markets.map((market) => (
                            <MenuItem 
                                key={market.id} 
                                value={market.id}
                                disabled={!market.enabled}
                                sx={{ 
                                    opacity: market.enabled ? 1 : 0.5,
                                    '&.Mui-disabled': {
                                        opacity: 0.5
                                    }
                                }}
                            >
                                {market.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <Button 
                    variant="contained" 
                    onClick={handleSearch}
                    disabled={!selectedMarket || selectedMarket !== 'nova'}
                    sx={{ 
                        py: 1.5,
                        px: 4,
                        minWidth: '100px'
                    }}
                >
                    Search
                </Button>
            </Box>
        </Box>
    );
};

export default HomePage; 