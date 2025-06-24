"use client";

import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";

export default function AiInsightModal({ name, description, onClose }) {
  return (
    <Dialog open={!!name} onClose={onClose} className="relative z-50">
      <DialogBackdrop className="fixed inset-0 bg-gray-400/50 bg-opacity-50" />

      <div className="fixed inset-0 overflow-y-auto">
        <div className="flex min-h-full items-center justify-center p-4 text-center">
          <DialogPanel className="relative transform overflow-hidden rounded-lg bg-slate-900 px-6 pt-5 pb-6 text-left shadow-xl transition-all max-w-lg w-full">
            <button
              onClick={onClose}
              className="absolute top-3 right-3 text-gray-400 hover:text-white focus:outline-none"
              aria-label="Close modal"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>

            <div className="flex items-center space-x-4">
            
 
              <DialogTitle className="text-white text-2xl font-bold">{name} - AI Insight ✨</DialogTitle>
            </div>

            <p className="mt-4 text-gray-300">{description}</p>

            <div className="mt-6 text-right">
              <button
                onClick={onClose}
                className="inline-flex justify-center rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none"
              >
                Close
              </button>
            </div>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
  );
}

