// Loading spinner component used across the app to show loading states
// Displays an animated spinning circle with optional message text
// Default message is "Loading..." but can be customized via props
function LoadingSpinner({ message = "Loading..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      {/* Animated spinning circle with orange border */}
      <div className="h-14 w-14 border-4 border-orange-400 border-t-transparent rounded-full animate-spin" />
      {/* Loading message text displayed below spinner */}
      <p className="mt-4 text-lg font-medium text-gray-700">{message}</p>
    </div>
  );
}

// Export LoadingSpinner component for use throughout the application
export default LoadingSpinner;
