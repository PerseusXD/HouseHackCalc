import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

interface ListingBlockProps {
    formattedAddress: string;
    city: string;
    state: string;
    zipCode: string;
    price: number;
    bedrooms?: number;
    bathrooms?: number;
    squareFootage?: number;
}

const ListingBlock: React.FC<ListingBlockProps> = ({
    formattedAddress,
    city,
    state,
    zipCode,
    price,
    bedrooms,
    bathrooms,
    squareFootage
}) => {
    return (
        <Card sx={{ 
            width: '100%', 
            maxWidth: '50%', 
            mb: 1.5,
            backgroundColor: '#f5f5f5',
            '&:hover': {
                backgroundColor: '#e0e0e0',
                transition: 'background-color 0.3s'
            }
        }}>
            <CardContent sx={{ py: 1.5, px: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ flex: 1, pr: 2 }}>
                        <Typography variant="subtitle1" gutterBottom sx={{ mb: 0.5 }}>
                            {formattedAddress}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            {city}, {state} {zipCode}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1.5 }}>
                            {bedrooms && (
                                <Typography variant="body2">
                                    {bedrooms} {bedrooms === 1 ? 'Bed' : 'Beds'}
                                </Typography>
                            )}
                            {bathrooms && (
                                <Typography variant="body2">
                                    {bathrooms} {bathrooms === 1 ? 'Bath' : 'Baths'}
                                </Typography>
                            )}
                            {squareFootage && (
                                <Typography variant="body2">
                                    {squareFootage.toLocaleString()} sqft
                                </Typography>
                            )}
                        </Box>
                    </Box>
                    <Typography variant="h6" color="primary" sx={{ ml: 2, whiteSpace: 'nowrap' }}>
                        ${price.toLocaleString()}
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
};

export default ListingBlock; 