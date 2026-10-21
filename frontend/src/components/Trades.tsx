import React from 'react';
import { Trade } from '../hooks/useMarketData';

interface TradesProps {
  trades: Trade[];
}

const TradesComponent: React.FC<TradesProps> = ({ trades }) => {
  const formatPrice = (price: number) => price.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const formatSize = (size: number) => size.toLocaleString('en-US', { minimumFractionDigits: 3, maximumFractionDigits: 3 });

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
    return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm shadow-lg w-full h-[600px] flex flex-col">
      <h2 className="text-xl font-bold mb-4 text-white">Recent Trades</h2>

      <div className="flex justify-between text-gray-500 mb-2 font-bold px-2">
        <span className="w-1/3">Time</span>
        <span className="w-1/3 text-right">Price</span>
        <span className="w-1/3 text-right">Size</span>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
        {trades.length === 0 ? (
          <div className="text-gray-400 text-center mt-4">Waiting for trades...</div>
        ) : (
          <div className="flex flex-col space-y-1">
            {trades.map((trade, idx) => (
              <div key={trade.trade_id || idx} className="flex justify-between px-2 py-1 hover:bg-gray-800 rounded">
                <span className="text-gray-400 w-1/3">{formatTime(trade.timestamp)}</span>
                <span className={`w-1/3 text-right ${trade.side === 'Buy' ? 'text-green-500' : 'text-red-500'}`}>
                  {formatPrice(trade.price)}
                </span>
                <span className="text-gray-300 w-1/3 text-right">{formatSize(trade.size)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1f2937;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #4b5563;
          border-radius: 3px;
        }
      `}} />
    </div>
  );
};

export default TradesComponent;
