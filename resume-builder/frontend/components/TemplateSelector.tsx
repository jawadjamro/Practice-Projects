'use client';

interface TemplateSelectorProps {
  selectedTemplate: string;
  onSelectTemplate: (template: string) => void;
}

const templates = [
  {
    id: 'modern',
    name: 'Modern',
    description: 'Clean and contemporary design',
  },
  {
    id: 'classic',
    name: 'Classic',
    description: 'Traditional professional style',
  },
  {
    id: 'minimal',
    name: 'Minimal',
    description: 'Simple and elegant layout',
  },
];

export default function TemplateSelector({
  selectedTemplate,
  onSelectTemplate,
}: TemplateSelectorProps) {
  return (
    <div className="space-y-4">
      <label className="block text-sm font-medium text-gray-700">
        Select Template
      </label>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {templates.map((template) => (
          <button
            key={template.id}
            type="button"
            onClick={() => onSelectTemplate(template.id)}
            className={`relative rounded-lg border-2 p-4 text-left transition-all ${
              selectedTemplate === template.id
                ? 'border-blue-600 bg-blue-50'
                : 'border-gray-200 bg-white hover:border-gray-300'
            }`}
          >
            <div className="mb-2 flex items-center gap-2">
              <div
                className={`h-3 w-3 rounded-full ${
                  selectedTemplate === template.id
                    ? 'bg-blue-600'
                    : 'bg-gray-300'
                }`}
              ></div>
              <span className="font-medium text-gray-900">
                {template.name}
              </span>
            </div>
            <p className="text-sm text-gray-500">{template.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
