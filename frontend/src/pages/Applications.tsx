import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/toast'

type AppItem = {
  id: number
  status: string
  created_at: string
  job: { title: string, company?: { name: string } }
}

export default function Applications() {
  const [apps, setApps] = useState<AppItem[]>([])
  const { add } = useToast()

  const load = async () => {
    const { data } = await api.get('/applications/applications/')
    setApps(data?.results ?? data)
  }

  useEffect(() => { load() }, [])

  const apply = async (id: number) => {
    const { data } = await api.post(`/applications/applications/${id}/apply/`)
    add({ title: 'Application queued', description: `Task ${data.task_id}` })
  }

  const tailorCover = async (id: number) => {
    await api.post(`/applications/applications/${id}/tailor-cover/`, { tone: 'professional' })
    add({ title: 'Cover letter tailored' })
    await load()
  }

  const tailorResume = async (id: number) => {
    await api.post(`/applications/applications/${id}/tailor-resume/`)
    add({ title: 'Resume tailored' })
    await load()
  }

  return (
    <div className="grid gap-6">
      <h2 className="text-xl font-semibold">Applications</h2>
      <div className="grid gap-4">
        {apps.map(a => (
          <Card key={a.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>{a.job.title} {a.job.company?.name ? `· ${a.job.company.name}` : ''}</span>
                <span className="text-sm text-muted-foreground">{a.status}</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground">Created {new Date(a.created_at).toLocaleString()}</div>
              <div className="mt-3 flex items-center gap-2">
                <Button onClick={() => apply(a.id)}>Apply</Button>
                <Button variant="secondary" onClick={() => tailorCover(a.id)}>Tailor Cover</Button>
                <Button variant="outline" onClick={() => tailorResume(a.id)}>Tailor Resume</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
