'use client';

import { useForm, useFieldArray } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { useResumeStore } from '@/store/resumeStore';
import { generateResume } from '@/lib/api';
import { ResumeRequest } from '@/types/resume';
import TemplateSelector from './TemplateSelector';
import SkillsInput from './SkillsInput';
import ExperienceSection from './ExperienceSection';
import EducationSection from './EducationSection';
import Loader from './Loader';

const defaultPersonalInfo = {
  full_name: '',
  email: '',
  phone: '',
  location: '',
  linkedin: '',
  portfolio: '',
};

export default function ResumeForm() {
  const router = useRouter();
  const { setResumeData, setOptimizedData, setLoading, setError } =
    useResumeStore();

  const form = useForm<ResumeRequest>({
    defaultValues: {
      personal_info: defaultPersonalInfo,
      summary: '',
      skills: [],
      experience: [],
      education: [],
      job_description: '',
      template: 'modern',
    },
  });

  const { control, register, handleSubmit, watch, setValue } = form;
  const template = watch('template');
  const skills = watch('skills');
  const jobDescription = watch('job_description');

  const {
    fields: experienceFields,
    append: appendExperience,
    remove: removeExperience,
  } = useFieldArray({
    control,
    name: 'experience',
  });

  const {
    fields: educationFields,
    append: appendEducation,
    remove: removeEducation,
  } = useFieldArray({
    control,
    name: 'education',
  });

  const onSubmit = async (data: ResumeRequest) => {
    setLoading(true);
    setError(null);
    setResumeData(data);

    try {
      const response = await generateResume(data);
      setOptimizedData(response);
      router.push('/preview');
    } catch (error) {
      setError(
        error instanceof Error ? error.message : 'Failed to generate resume'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Personal Information */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-gray-900">
          Personal Information
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Full Name *
            </label>
            <input
              {...register('personal_info.full_name', {
                required: 'Full name is required',
              })}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="John Doe"
            />
            {form.formState.errors.personal_info?.full_name && (
              <p className="mt-1 text-xs text-red-500">
                {form.formState.errors.personal_info.full_name.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Email *
            </label>
            <input
              {...register('personal_info.email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              type="email"
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="john@example.com"
            />
            {form.formState.errors.personal_info?.email && (
              <p className="mt-1 text-xs text-red-500">
                {form.formState.errors.personal_info.email.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Phone *
            </label>
            <input
              {...register('personal_info.phone', {
                required: 'Phone is required',
              })}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="+1-234-567-8900"
            />
            {form.formState.errors.personal_info?.phone && (
              <p className="mt-1 text-xs text-red-500">
                {form.formState.errors.personal_info.phone.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Location *
            </label>
            <input
              {...register('personal_info.location', {
                required: 'Location is required',
              })}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="San Francisco, CA"
            />
            {form.formState.errors.personal_info?.location && (
              <p className="mt-1 text-xs text-red-500">
                {form.formState.errors.personal_info.location.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              LinkedIn
            </label>
            <input
              {...register('personal_info.linkedin')}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="linkedin.com/in/johndoe"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Portfolio
            </label>
            <input
              {...register('personal_info.portfolio')}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="johndoe.com"
            />
          </div>
        </div>
      </section>

      {/* Professional Summary */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-gray-900">
          Professional Summary
        </h2>
        <textarea
          {...register('summary', {
            required: 'Professional summary is required',
            minLength: {
              value: 20,
              message: 'Summary must be at least 20 characters',
            },
          })}
          rows={4}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          placeholder="Write a brief professional summary highlighting your key strengths and career goals..."
        />
        {form.formState.errors.summary && (
          <p className="mt-1 text-xs text-red-500">
            {form.formState.errors.summary.message}
          </p>
        )}
      </section>

      {/* Skills */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-gray-900">Skills</h2>
        <SkillsInput
          skills={skills}
          onChange={(newSkills) => setValue('skills', newSkills)}
        />
      </section>

      {/* Experience */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <ExperienceSection
          form={form}
          fields={experienceFields}
          onAdd={() =>
            appendExperience({
              company: '',
              role: '',
              start_date: '',
              end_date: '',
              responsibilities: '',
            })
          }
          onRemove={removeExperience}
        />
      </section>

      {/* Education */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <EducationSection
          form={form}
          fields={educationFields}
          onAdd={() =>
            appendEducation({
              degree: '',
              institution: '',
              year: '',
            })
          }
          onRemove={removeEducation}
        />
      </section>

      {/* Job Description (Optional) */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-gray-900">
          Target Job Description (Optional)
        </h2>
        <textarea
          {...register('job_description')}
          rows={4}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          placeholder="Paste the job description you're targeting to help tailor your resume..."
        />
        <p className="mt-2 text-sm text-gray-500">
          This helps customize your resume for the specific role.
        </p>
      </section>

      {/* Template Selector */}
      <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <TemplateSelector
          selectedTemplate={template}
          onSelectTemplate={(t) => setValue('template', t)}
        />
      </section>

      {/* Submit Button */}
      <div className="flex items-center justify-center">
        <button
          type="submit"
          disabled={form.formState.isSubmitting}
          className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-4 font-semibold text-white shadow-lg transition-all hover:from-blue-700 hover:to-blue-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {form.formState.isSubmitting ? (
            <>
              <Loader />
              <span>Generating Resume...</span>
            </>
          ) : (
            <span>Generate Resume</span>
          )}
        </button>
      </div>
    </form>
  );
}
