import React from 'react';
import { OrderBook } from '../hooks/useMarketData';

interface OrderBookProps {
  orderBook: OrderBook | null;
}

const OrderBookComponent: React.FC<OrderBookProps> = ({ orderBook }) => {
  if (!orderBook) {
    return <div className="text-gray-400 p-4">Waiting for order book data...</div>;
  }

  // Format numbers for better readability
  const formatPrice = (price: number) => price.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const formatSize = (size: number) => size.toLocaleString('en-US', { minimumFractionDigits: 3, maximumFractionDigits: 3 });

  return (
    <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm shadow-lg w-full">
      <h2 className="text-xl font-bold mb-4 text-white">Order Book ({orderBook.symbol})</h2>

      <div className="flex justify-between text-gray-500 mb-2 font-bold px-2">
        <span>Price (USDT)</span>
        <span>Size</span>
      </div>

      <div className="flex flex-col gap-1">
        {/* Asks (Sells) - Reversed to show highest price at top */}
        <div className="flex flex-col-reverse space-y-reverse space-y-1">
          {orderBook.asks.slice(0, 15).map((ask, idx) => (
            <div key={`ask-${idx}`} className="flex justify-between px-2 py-0.5 hover:bg-gray-800 rounded">
              <span className="text-red-500">{formatPrice(ask.price)}</span>
              <span className="text-gray-300">{formatSize(ask.size)}</span>
            </div>
          ))}
        </div>

        {/* Spread / Mid-market indicator */}
        <div className="my-2 py-2 border-y border-gray-700 text-center font-bold text-gray-400 flex justify-center gap-4">
           {orderBook.asks.length > 0 && orderBook.bids.length > 0 && (
             <span>Spread: {formatPrice(orderBook.asks[0].price - orderBook.bids[0].price)}</span>
           )}
        </div>

        {/* Bids (Buys) */}
        <div className="flex flex-col space-y-1">
          {orderBook.bids.slice(0, 15).map((bid, idx) => (
            <div key={`bid-${idx}`} className="flex justify-between px-2 py-0.5 hover:bg-gray-800 rounded">
              <span className="text-green-500">{formatPrice(bid.price)}</span>
              <span className="text-gray-300">{formatSize(bid.size)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OrderBookComponent;
