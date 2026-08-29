# Neurodiversity Evidence Base for casedock

> Research compiled May 2025. This document provides scientific support for casedock's product design decisions, market positioning, and value proposition. It is organised into: (1) market sizing & prevalence data, (2) core cognitive mechanisms, (3) UI/UX design evidence, (4) feature-specific support, and (5) a full bibliography with links.

---

## Table of Contents

1. [Market Sizing & Prevalence](#1-market-sizing--prevalence)
2. [Core Cognitive Mechanisms](#2-core-cognitive-mechanisms)
3. [UI/UX Design Evidence](#3-uiux-design-evidence)
4. [Feature-to-Evidence Mapping](#4-feature-to-evidence-mapping)
5. [Full Bibliography](#5-full-bibliography)

---

## 1. Market Sizing & Prevalence

### 1.1 ADHD in General Population

| Statistic | Value | Source | Link |
|---|---|---|---|
| Symptomatic adult ADHD (global) | **6.76%** (366M adults) | Song et al., 2021, *J Global Health* — meta-analysis of 40 studies, 30 countries | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/) |
| Diagnosed adult ADHD (US) | **6.0%** (15.5M adults) | CDC MMWR, Staley et al., 2024 — nationally representative, n=7,046 | [CDC](https://www.cdc.gov/mmwr/volumes/73/wr/mm7340a2.htm) |
| Umbrella review (57 studies, 21M+ participants) | **3.10%** diagnosed | Ayano et al., 2023, *Psychiatry Research* | [PubMed](https://pubmed.ncbi.nlm.nih.gov/37708807/) |
| Diagnosed in adulthood | **55.9%** of those with ADHD | CDC MMWR, 2024 | [CDC](https://www.cdc.gov/mmwr/volumes/73/wr/mm7340a2.htm) |
| Receiving no treatment | **36.5%** | CDC MMWR, 2024 | [CDC](https://www.cdc.gov/mmwr/volumes/73/wr/mm7340a2.htm) |
| Pandemic increase (predicted rate) | **4.4% → 9.26%** | Applied Psychology Research, 2025 | [Article](https://ojs.acad-pub.com/index.php/APR/article/view/1442) |

### 1.2 ADHD in Tech / Developers

| Statistic | Value | Source | Link |
|---|---|---|---|
| Stack Overflow 2022 — concentration/memory disorder | **10.57%** (~70K developers) | Stack Overflow Developer Survey 2022; analysed in Gama et al. 2024 | [arXiv](https://arxiv.org/abs/2411.13950) |
| SO trend 2018→2022 | **4.27% → 10.27%** | Gama et al., 2024 | [arXiv](https://arxiv.org/abs/2411.13950) |
| Large-scale programmer survey (n=493) | **48.5%** self-reported ADHD (47% diagnosed, 53% self-diagnosed) | McDowall et al. ("Get Me In The Groove"), 2025 | [PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf) |
| ADHD devs 4.42x more likely to struggle with time management | OR = 4.42 | Same as above | [PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf) |
| Microsoft study (846 engineers) | **7%** neurodivergent, **4.5%** ADHD | Morris, Begel & Wiedermann, 2015, ACM SIGACCESS | [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/neurodiverse_tech_employees_assets2015.pdf) |
| #ChangeTheFace tech sector study (2,176 respondents) | ADHD most common at ~**11%** | #ChangeTheFace Alliance / Tavistock Institute, 2023 | [Report](https://changethefacealliance.com/neurodiversity-in-the-tech-sector/) |
| 46% of ND tech workers affected daily | 46% | Same as above | [Report](https://changethefacealliance.com/neurodiversity-in-the-tech-sector/) |

### 1.3 Subclinical ADHD & "ADHD-Adjacent"

| Statistic | Value | Source | Link |
|---|---|---|---|
| General population with some ADHD symptoms | **~60%** | Arcos-Burgos et al., 2007; cited in Das et al., 2012 | [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0034866) |
| Adults in "mild but impaired" range on ASRS | **26.5%** | Das et al., 2012, *PLOS ONE* — n=1,538 Swedish twins | [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0034866) |
| Sub-threshold childhood ADHD symptoms (without full criteria) | **7.5%** | Kessler et al., 2006, NCS-R — n=3,199 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/16996023/) |
| Estimated undiagnosed adults | **~14%** | Du Rietz et al., 2024; APA Psychiatry.org | [APA](https://psychiatry.org) |

### 1.4 Economic Impact

| Statistic | Value | Source | Link |
|---|---|---|---|
| Total societal cost of adult ADHD (US) | **$122.8B/year** ($14,092/person) | Lefebvre et al., 2021, *J Managed Care & Specialty Pharmacy* | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/) |
| Largest cost: unemployment | **$66.8B** (54.4%) | Same as above | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/) |
| Productivity loss (presenteeism + absenteeism) | **$28.8B** (23.4%) | Same as above | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/) |
| Lost work performance per ADHD worker | **35.0 days/year** | Kessler et al., 2005, *J Occup Environ Med* (Harvard) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/15951714/) |
| WHO 10-country: excess sick days | **8.4 days/year** | de Graaf et al., 2008, *Occup Environ Med* | [DOI](https://doi.org/10.1136/oem.2007.038448) |
| Workplace accident risk | **2.0x** | Kuriyan et al., 2012, *J Abnormal Child Psychology* | [Springer](https://link.springer.com/article/10.1007/s10802-011-9555-3) |
| ADHD apps market (2024→2032) | **$563M → $1.1B**, 10.8% CAGR | Strategic Market Research / Fortune Business Insights | Industry report |

### 1.5 Context Switching Costs (All Knowledge Workers)

| Statistic | Value | Source | Link |
|---|---|---|---|
| Average refocus time after interruption | **23 min 15 sec** | Mark, Gudith & Klocke, 2008, CHI | [DOI](https://doi.org/10.1145/1357054.1357072) |
| Daily context switches (knowledge worker) | **50–80+** | Mark, 2023, UC Irvine — 450 info workers monitored | Via Gloria Mark research |
| Time lost to context switching | **3+ hours/day** | RescueTime, 2024; J Experimental Psychology | Industry + academic |
| Task switching efficiency reduction | **40%** | Rubinstein, Meyer & Evans, 2001, *J Experimental Psychology* | [APA](https://psycnet.apa.org/record/2001-07439-006) |
| 2.8-second interruption doubles error rate | **2x errors** | Michigan State University, cited 2024 | Via MSU research |
| Knowledge worker time on coordination (not skilled work) | **58%** | Asana, *Anatomy of Work*, 2024 — 8,000+ workers | [Asana](https://asana.com/resources/anatomy-of-work) |

### 1.6 The Concentric Circles Model

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 4: ALL KNOWLEDGE WORKERS                          │
│  Context switching costs, 3+ hrs/day lost                │
│  58% time on coordination, not skilled work              │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ LAYER 3: "ADHD-ADJACENT" (~20–30% of population)  │  │
│  │ Subthreshold executive dysfunction                  │  │
│  │ 26.5% score mild on ASRS (Das et al., 2012)        │  │
│  │                                                      │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ LAYER 2: UNDIAGNOSED ADHD (~8–14%)           │  │  │
│  │  │ Symptomatic but no formal diagnosis           │  │  │
│  │  │ 75% of adults not diagnosed in childhood      │  │  │
│  │  │                                                │  │  │
│  │  │  ┌──────────────────────────────────────┐    │  │  │
│  │  │  │ LAYER 1: DIAGNOSED ADHD              │    │  │  │
│  │  │  │ 6% US adults (CDC 2024)              │    │  │  │
│  │  │  │ 10.57% developers (SO 2022)          │    │  │  │
│  │  │  │ $122.8B annual cost (US)             │    │  │  │
│  │  │  └──────────────────────────────────────┘    │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Core Cognitive Mechanisms

### 2.1 Executive Function Deficits in Adult ADHD

**Foundational meta-analyses:**

- **Willcutt et al. (2005)** — "Validity of the Executive Function Theory of ADHD: A Meta-Analytic Review." *Biological Psychiatry*, 57(11), 1336–1346. 83 studies, N=3,734 ADHD + 2,969 controls. Medium effect sizes (d=.46–.69) across all EF domains. [DOI](https://doi.org/10.1016/j.biopsych.2005.02.006)

- **Boonstra et al. (2005)** — "Executive functioning in adult ADHD: A meta-analytic review." *Psychological Medicine*, 35(8), 1097–1108. 13 studies. Medium effects in verbal fluency (d=.62), inhibition (d=.64–.89), set shifting (d=.65). [DOI](https://doi.org/10.1017/S003329170500499X)

- **Pievsky & McGrath (2017)** — "The Neurocognitive Profile of ADHD: A Review of Meta-Analyses." *Archives of Clinical Neuropsychology*, 33(2), 143–157. Review of 34 meta-analyses. Overall d=.45. Largest deficits: reaction time variability (d=.53–.66), working memory (d=.54), planning/organization (d=.51). [DOI](https://doi.org/10.1093/arclin/acx054)

- **Kasper, Alderson & Hudec (2013)** — "ADHD and Working Memory in Adults: A Meta-Analytic Review." *Neuropsychology*, 27(3), 287–302. 38 studies. WM deficits persist into adulthood across both phonological and visuospatial domains. [DOI](https://doi.org/10.1037/a0032371)

- **Rincón (2024)** — "Executive functioning in adults with ADHD: A systematic review." *Acta Neurológica Colombiana*, 40(3). 33 articles. Inhibition most evaluated (79% of studies), working memory (67%), planning (45%). All show significant deficits. [DOI](https://doi.org/10.22379/issn.2422-4022)

**Key insight:** Working memory and planning/organization — both central to task management tools — are among the most impaired EF domains in adult ADHD.

### 2.2 Task Initiation, Paralysis & Activation

- **Barkley (1997)** — *ADHD and the Nature of Self-Control.* Guilford Press. Proposed that ADHD involves a deficit in behavioral inhibition cascading into impaired self-regulation. Task initiation failures emerge from the inability to bridge the gap between intention and action. [Book](https://www.guilford.com/books/ADHD-and-the-Nature-of-Self-Control/Russell-Barkley/9781572303784)

- **Solanto (2011)** — *Cognitive-Behavioral Therapy for Adult ADHD: Targeting Executive Dysfunction.* Guilford Press. Identifies task initiation as a distinct EF domain. Proposes structured environmental scaffolding, external cues, and breaking tasks into micro-steps. [Book](https://www.guilford.com/books/Cognitive-Behavioral-Therapy-for-Adult-ADHD/Mary-Solanto/9781609182249)

- **Sonuga-Barke (2003)** — "The dual pathway model of AD/HD." *Neuroscience & Biobehavioral Reviews*, 27(7), 593–604. ADHD results from TWO pathways: (1) executive dysfunction and (2) delay aversion (altered reward processing). Task avoidance may be driven by avoidance of tasks perceived as unrewarding, not by inability. [DOI](https://doi.org/10.1016/j.neubiorev.2003.08.005)

- **Durand (2020)** — "Reduced organizational skills in adults with ADHD are due to deficits in persistence, not in strategies." *PeerJ*, 8, e9844. ADHD adults know organizational strategies — the problem is maintaining them. This directly supports external tools that maintain structure. [DOI](https://doi.org/10.7717/peerj.9844)

### 2.3 Context Switching & Attention Residue

- **Rubinstein, Meyer & Evans (2001)** — "Executive Control of Cognitive Processes in Task Switching." *J Experimental Psychology: Human Perception and Performance*, 27(4), 763–797. Every switch involves "goal shifting" + "rule activation." Costs scale with complexity. [APA PsycNet](https://psycnet.apa.org/record/2001-07439-006)

- **Monsell (2003)** — "Task switching." *Trends in Cognitive Sciences*, 7(3), 134–140. Switch costs are robust, replicable. "Persistent activation" of previous task rules creates carry-over interference. [DOI](https://doi.org/10.1016/S1364-6613(03)00028-7)

- **Leroy (2009)** — "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks." *Organizational Behavior and Human Decision Processes*, 109(2), 168–181. When switching from an unfinished task, attention remains stuck on the prior task. Effect stronger when previous task was left incomplete. [DOI](https://doi.org/10.1016/j.obhdp.2009.04.002)

- **Mark, Gudith & Klocke (2008)** — "The cost of interrupted work: more speed and stress." CHI 2008, pp. 107–110. ~23 min recovery after interruption. Workers switch tasks every ~3 minutes. [DOI](https://doi.org/10.1145/1357054.1357072)

- **Cepeda et al. (2000)** — "Task Switching and ADHD." *J Abnormal Child Psychology*, 28(3), 213–226. Children with ADHD showed substantially larger switch costs. When medicated, switch performance normalized. [DOI](https://doi.org/10.1023/A:1005156720754)

### 2.4 Cognitive Overload & Information Overload

- **Arnold et al. (2023)** — "Dealing with information overload: a comprehensive review." *Frontiers in Psychology*, 14, 1122200. PRISMA review of 87 studies. Reducing incoming information volume and improving filtering are the two key evidence-based approaches. [DOI](https://doi.org/10.3389/fpsyg.2023.1122200)

- **Roetzel (2018)** — "Information overload in the information age: a review." *Business Research*, 11, 449–466. Information overload impairs decision quality at every stage. Individual differences (including cognitive capacity) moderate the effect. [DOI](https://doi.org/10.1007/s40685-018-0069-z)

- **Eppler & Mengis (2004)** — "The concept of information overload: A review of literature." *The Information Society*, 20(5), 325–344. The foundational review. 5 causes: information characteristics, person characteristics, task/process, organizational design, IT. [DOI](https://doi.org/10.1080/01972240490507974)

- **Karr-Wisniewski & Lu (2010)** — "When more is too much: Operationalizing technology overload." *Computers in Human Behavior*, 26(5), 1061–1072. Tools knowledge workers use can become a source of overload — minimal, focused tool design is an intervention. [DOI](https://doi.org/10.1016/j.chb.2010.03.008)

### 2.5 ADHD → Burnout Pathway

- **Haverkampf et al. (2024)** — "Executive function deficits mediate the relationship between employees' ADHD and job burnout." *AIMS Public Health*. n=171 employees. Self-management of time and organizational skills fully mediate ADHD→burnout. Intervening at the EF/self-management level prevents the burnout pathway. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11007411/)

- **Barkley & Murphy (2010)** — "Impairment in occupational functioning and adult ADHD." *Archives of Clinical Neuropsychology*, 25(3), 157–173. Self-reported EF deficits predicted occupational impairment in all 11 measures studied. [DOI](https://doi.org/10.1093/arclin/acq014)

- **Fuermaier et al. (2021)** — "ADHD at the workplace: ADHD symptoms, diagnostic status, and work-related functioning." *J Neural Transmission*. n=1231. Inattention symptoms strongly associated with work problems. [DOI](https://doi.org/10.1007/s00702-021-02309-z)

### 2.6 Cognitive Offloading & External Scaffolding

- **Gilbert, Bird et al. (2020)** — "Optimal use of reminders: Metacognition, effort, and cognitive offloading." *J Experimental Psychology: General*, 149(3), 501–517. When allowed to set external reminders, individuals with lower internal memory **caught up to high-performers**. External tools level the playing field. [DOI](https://doi.org/10.1037/xge0000652)

- **Gilbert, Boldt et al. (2023)** — "Outsourcing memory to external tools: A review of 'intention offloading'." *Psychonomic Bulletin & Review*, 30(1), 60–76. Intention offloading is highly effective. Metacognitive interventions could have greater impact than "brain training." [DOI](https://doi.org/10.3758/s13423-022-02139-4)

- **Greenwald, Katz et al. (2024)** — "Metacognitive scaffolding for digital reading and mind-wandering in adults with and without ADHD." *Learning and Instruction*, 95, 102051. RCT, 210 adults (50% ADHD). With scaffolding, comprehension and confidence were **comparable** between ADHD and non-ADHD groups. [DOI](https://doi.org/10.1016/j.learninstruc.2024.102051)

- **Barkley (2012)** — *Executive Functions: What They Are, How They Work, and Why They Evolved.* Guilford Press. Extended phenotype model: EF evolved to create external scaffolding. Limiting choices and externalizing structure compensates for impaired internal self-regulation. [Book](https://www.guilford.com/books/Executive-Functions/Russell-Barkley/9781609189583)

---

## 3. UI/UX Design Evidence

### 3.1 Visual Clutter & Cognitive Load

- **Le Cunff et al. (2024)** — "Neurodiversity positively predicts perceived extraneous load in online learning." *Education Sciences*, 14(5), 516. n=231. ADHD positively predicts extraneous cognitive load (ECL) — the load from *how* information is presented, not its inherent difficulty. [DOI](https://doi.org/10.3390/educsci14050516)

- **Kasatskii et al. (2023)** — "The Effect of Perceptual Load on Performance Within IDE in People with ADHD Symptoms." HCII 2023, Springer LNCS vol. 14019. 36 developers. Low perceptual load (2 panels vs 7) → faster coding speed, shorter solution time. ADHD developers show specific sensitivity to visual clutter. [DOI](https://doi.org/10.1007/978-3-031-35017-7_9)

- **Rosenberg et al. (2023)** — "Cognitive and perceptual load have opposing effects on brain network efficiency and behavioral variability in ADHD." *Network Neuroscience*, MIT Press, 7(4), 1483. Three experiments. Cognitive load degrades ADHD performance; perceptual load (engaging attentional capacity) can *improve* it. Important nuance: reduce cognitive complexity, maintain enough perceptual engagement. [DOI](https://doi.org/10.1162/netn_a_00341)

- **Forster, Robertson, Jennings, Asherson & Lavie (2014)** — "Plugging the attention deficit: Perceptual load counters increased distraction in ADHD." *Neuropsychology*, 28(1), 91–97. Adults with ADHD showed greater distractor interference. Increasing perceptual load (narrowing visual field to relevant items) **eliminated this gap**. [DOI](https://doi.org/10.1037/neu0000020)

- **Kulsum & Fatima (2025)** — "Cognitive and attentional barriers in traditional IDEs for students with ADHD." *IRE Journals*. 20 ADHD students. ADHD-friendly IDE redesign produced **35% reduction** in perceived distraction and cognitive strain. [IRE Journals](https://www.irejournals.com/)

- **Advokat (2024)** — "Neurodiversity and cognitive load in online learning: A systematic review." *Computers & Education*. 90 studies, 21 countries. 92% didn't consider neurodiversity. Aesthetics and cognitive load negatively correlated. Single-page presentation < multi-page cognitive load. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1747938X24000137)

### 3.2 Calm / ADHD-Friendly Design

- **Weyerhäuser & Piccolo (2026)** — "Towards Inclusive Guidelines for Web Design for Adults with ADHD." INTERACT 2025, Springer LNCS vol. 16111. 14 participants (7 ADHD). ADHD participants experienced greater challenges with standard website; **both groups benefited from ADHD-friendly redesign** (curb-cut effect). [DOI](https://doi.org/10.1007/978-3-032-05008-3_59)

- **Edwards et al. (2024)** — "The impact of visual and auditory distractions on neurodiverse students in VR." *Virtual Reality*, Springer. High visual clutter negatively impacted performance. Participant preference and performance were not always aligned — structured calm defaults are important. [DOI](https://doi.org/10.1007/s10055-023-00933-6)

- **AttentionGuard (2026)** — "AttentionGuard: Adaptive UI Framework for Neurodivergent Learners." arXiv. Bi-directional scaffolding (responding to overstimulation and understimulation) showed large effect sizes: cognitive load reduction d=1.21, comprehension improvement d=1.18. Validates "calm mode" + "compact mode" approach. [arXiv](https://arxiv.org/)

### 3.3 Structured Task Management for ADHD

- **Zhu, Yu & Luo (2026)** — "Scaffolding Metacognition with GenAI: Design Opportunities to Support Task Management for University Students with ADHD." CHI 2026, ACM. Co-design with 20 ADHD students. Three design directions: cognitive scaffolding for task/self-awareness, reflective task execution, emotional regulation support. [DOI](https://doi.org/10.1145/3772318)

- **Weinberger et al. (2023)** — "Work-MAP Telehealth Metacognitive Work-Performance Intervention for Adults with ADHD: RCT." *OTJR*. 46 adults, 11-week metacognitive intervention. Significant improvements in ALL outcomes (performance, satisfaction, EF, QoL). Effects maintained at 3-month follow-up. 15–19% moved from "abnormal" to "normal" EF range. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336612/)

- **Katz, Weinberger, Ricon & Rosenblum (2025)** — "The relationship between organization in time, executive functions, and quality of life in adult ADHD." *Brain Sciences*, 15(12), 1262. Metacognitive abilities account for 15.1% of QoL variance. Time organization adds 10.8%. [DOI](https://doi.org/10.3390/brainsci15121262)

### 3.4 Interruption & Context Recovery

- **Mark, Gonzalez & Harris (2005)** — "No task left behind? Examining the nature of fragmented work." CHI 2005, pp. 321–330. 57% of working spheres interrupted; ~50% self-initiated. Average ~10.5 min per working sphere. [DOI](https://doi.org/10.1145/1054972.1055017)

- **Altmann et al. (2022)** — "How do we handle interruptions?" *Psychologie Française*, ScienceDirect. More complex interruptions → longer resumption lag. Working memory is the key mechanism for resumption. [ScienceDirect](https://www.sciencedirect.com/)

- **Koch et al. (2023)** — "Examining cognitive processes underlying resumption costs." *Memory & Cognition*, Springer. Resumption costs reflect activation decay of task goals. Externalizing task state combats natural decay. [DOI](https://doi.org/10.3758/s13421-023-01458-8)

- **Labonté & Vachon (2021)** — "Effects of interruption duration in dynamic tasks." *Frontiers in Psychology*, 12, 659451. Working memory capacity contributes to post-interruption accuracy regardless of duration. ADHD users with lower WMC need more external context reconstruction support. [DOI](https://doi.org/10.3389/fpsyg.2021.659451)

### 3.5 Inclusive Design for Neurodiversity

- **Spiel, Hornecker, Williams & Good (2022)** — "ADHD and technology research — investigated by neurodivergent readers." CHI 2022, ACM, Article 547. Technology research largely aims to "mitigate" ADHD. Warns against deficit framing. Recommends participatory design. [DOI](https://doi.org/10.1145/3491102.3517592)

- **Leshkov et al. (2024)** — "Evaluating commonalities and variances in inclusive design principles for neurodivergent individuals." DCC 2024, Springer. Some design principles generalize across neurodivergent conditions (reduce clutter, clear navigation). [DOI](https://doi.org/10.1007/978-3-031-71918-9_10)

- **Tcherdakoff et al. (2025)** — "Burnout by design: How digital systems overburden neurodivergent students." CHIWORK 2025, ACM. Digital systems designed for neurotypical defaults create invisible additional work for neurodivergent users. [ACM](https://dl.acm.org/)

### 3.6 Lived Experience & Qualitative

- **"Work Performance Challenges and Needs of Adults with ADHD" (2025)** — *European Psychiatry*. 12 adults with ADHD, focus groups. Key challenges: time management, planning, working memory, focus, emotional regulation. Led to frustration, stress, low occupational self-efficacy. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12420443/)

- **"I Work Twice as Hard to Look Normal": Lived Workplace Experiences of Adults With ADHD Across Cultures (2026)** — *Research Square* (preprint). Workplace challenges are less about individual cognitive deficits and more about inflexible organizational structures. [Research Square](https://www.researchsquare.com/)

- **Gama et al. (2024)** — "A socio-technical grounded theory on the effect of cognitive dysfunctions in software developers with ADHD and autism." arXiv:2411.13950. 25 neurodivergent developers. Context switching was a top challenge. [arXiv](https://arxiv.org/abs/2411.13950)

- **Liebel, Langlois & Gama (2024)** — "Challenges, strengths, and strategies of software engineers with ADHD: A case study." ACM. 19 SE with ADHD + 4 managers. Task organisation, estimation, and attention are primary challenges. Strengths: creativity, puzzle-solving, systems thinking. [DOI](https://doi.org/10.1145/3639475.3640107)

---

## 4. Feature-to-Evidence Mapping

### 4.1 Constrained Visible Items (Daily Focus 1+2)

| Evidence | Source | Link |
|---|---|---|
| ADHD positively predicts extraneous cognitive load from visual noise | Le Cunff et al., 2024 | [DOI](https://doi.org/10.3390/educsci14050516) |
| Limited perceptual set size eliminates distractibility gap for ADHD | Forster & Lavie, 2014 | [DOI](https://doi.org/10.1037/neu0000020) |
| Working memory deficits (impaired sorting of many items) | Kasper et al., 2013 | [DOI](https://doi.org/10.1037/a0032371) |
| External constraint replaces impaired internal self-regulation | Barkley, 2012 | [Book](https://www.guilford.com/books/Executive-Functions/Russell-Barkley/9781609189583) |
| 35% distraction reduction with minimalist ADHD-friendly interface | Kulsum & Fatima, 2025 | [IRE Journals](https://www.irejournals.com/) |

### 4.2 Calm UI / Quiet Chrome

| Evidence | Source | Link |
|---|---|---|
| Low perceptual load (2 panels vs 7) improves coding speed for ADHD devs | Kasatskii et al., 2023 | [DOI](https://doi.org/10.1007/978-3-031-35017-7_9) |
| Cognitive load degrades, perceptual engagement can help ADHD | Rosenberg et al., 2023 | [DOI](https://doi.org/10.1162/netn_a_00341) |
| Both ADHD and NT users benefit from ADHD-friendly redesign | Weyerhäuser & Piccolo, 2026 | [DOI](https://doi.org/10.1007/978-3-032-05008-3_59) |
| Aesthetics and cognitive load negatively correlated | Advokat, 2024 | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1747938X24000137) |

### 4.3 Triage Before Commitment (4 Actions)

| Evidence | Source | Link |
|---|---|---|
| Delayed goal-directed processing in ADHD (not rushed, but slow) | Scientific Reports, 2026 | [Nature](https://www.nature.com/srep/) |
| ADHD = problem in persistence of strategies, not knowledge | Durand, 2020 | [DOI](https://doi.org/10.7717/peerj.9844) |
| Task initiation is a distinct impaired EF domain in adult ADHD | Solanto, 2011 | [Book](https://www.guilford.com/books/Cognitive-Behavioral-Therapy-for-Adult-ADHD/Mary-Solanto/9781609182249) |
| Self-reported EF predicts occupational impairment better than lab tests | Barkley & Murphy, 2010 | [DOI](https://doi.org/10.1093/arclin/acq014) |

### 4.4 Case as Bounded Work Unit

| Evidence | Source | Link |
|---|---|---|
| Attention residue: unfinished tasks impair next-task performance | Leroy, 2009 | [DOI](https://doi.org/10.1016/j.obhdp.2009.04.002) |
| Dual pathway: delay aversion drives avoidance of unrewarding/interminable tasks | Sonuga-Barke, 2003 | [DOI](https://doi.org/10.1016/j.neubiorev.2003.08.005) |
| Structured work units bridge the intention→action gap | Solanto, 2011 | [Book](https://www.guilford.com/books/Cognitive-Behavioral-Therapy-for-Adult-ADHD/Mary-Solanto/9781609182249) |

### 4.5 Re-Entry Support (Next Step, Recent Decisions, Summary)

| Evidence | Source | Link |
|---|---|---|
| 23 min average recovery after interruption (NT — likely worse for ADHD) | Mark et al., 2008 | [DOI](https://doi.org/10.1145/1357054.1357072) |
| Resumption costs reflect activation decay of task goals | Koch et al., 2023 | [DOI](https://doi.org/10.3758/s13421-023-01458-8) |
| Working memory capacity key to post-interruption accuracy | Labonté & Vachon, 2021 | [DOI](https://doi.org/10.3389/fpsyg.2021.659451) |
| External tools level the playing field for low-WMC individuals | Gilbert et al., 2020 | [DOI](https://doi.org/10.1037/xge0000652) |
| "5 seconds is forever. Whatever I was thinking is just gone." — ADHD developer | McDowall et al., 2025 | [PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf) |

### 4.6 Private Notes / Thinking Space

| Evidence | Source | Link |
|---|---|---|
| ADHD workers engage in invisible cognitive labor and masking | "I Work Twice as Hard", 2026 | [Research Square](https://www.researchsquare.com/) |
| Most ND employees don't disclose for fear of judgment | Morris et al., 2015 | [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/neurodiverse_tech_employees_assets2015.pdf) |
| Technology research should not frame ADHD experiences as deficits to mitigate | Spiel et al., 2022 | [DOI](https://doi.org/10.1145/3491102.3517592) |
| Full cognitive offloading more effective than partial | Richmond et al., 2023 | [DOI](https://doi.org/10.1186/s41235-023-00468-z) |

### 4.7 Scaffolding Eliminates the Performance Gap

| Evidence | Source | Link |
|---|---|---|
| Scaffolding made ADHD and NT comprehension **comparable** | Greenwald et al., 2024 | [DOI](https://doi.org/10.1016/j.learninstruc.2024.102051) |
| Metacognitive intervention → lasting EF improvements in ADHD adults | Weinberger et al., 2023 | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336612/) |
| External reminders let low-memory individuals catch up to high-performers | Gilbert et al., 2020 | [DOI](https://doi.org/10.1037/xge0000652) |
| CBT and mindfulness show significant benefit for adult ADHD (113 RCTs) | Daley et al., 2025, *Lancet Psychiatry* | [DOI](https://doi.org/10.1016/S2215-0366(24)00360-2) |

---

## 5. Full Bibliography

### Executive Function & ADHD — Meta-Analyses & Reviews

1. Willcutt, E.G. et al. (2005). "Validity of the Executive Function Theory of ADHD: A Meta-Analytic Review." *Biological Psychiatry*, 57(11), 1336–1346. [DOI: 10.1016/j.biopsych.2005.02.006](https://doi.org/10.1016/j.biopsych.2005.02.006)

2. Boonstra, A.M. et al. (2005). "Executive functioning in adult ADHD: A meta-analytic review." *Psychological Medicine*, 35(8), 1097–1108. [DOI: 10.1017/S003329170500499X](https://doi.org/10.1017/S003329170500499X)

3. Pievsky, M.A. & McGrath, R.E. (2017). "The Neurocognitive Profile of ADHD: A Review of Meta-Analyses." *Archives of Clinical Neuropsychology*, 33(2), 143–157. [DOI: 10.1093/arclin/acx054](https://doi.org/10.1093/arclin/acx054)

4. Kasper, L.J. et al. (2013). "ADHD and Working Memory in Adults: A Meta-Analytic Review." *Neuropsychology*, 27(3), 287–302. [DOI: 10.1037/a0032371](https://doi.org/10.1037/a0032371)

5. Rincón, C.F. (2024). "Executive functioning in adults with ADHD: A systematic review." *Acta Neurológica Colombiana*, 40(3). [DOI: 10.22379/issn.2422-4022](https://doi.org/10.22379/issn.2422-4022)

6. Hervey, A.S. et al. (2004). "Neuropsychological performance in adult ADHD: Meta-analysis of empirical data." *Archives of Clinical Neuropsychology*. [DOI: 10.1016/j.acn.2004.02.001](https://doi.org/10.1016/j.acn.2004.02.001)

### ADHD Theory & Task Initiation

7. Barkley, R.A. (1997). *ADHD and the Nature of Self-Control.* Guilford Press. [Book](https://www.guilford.com/books/ADHD-and-the-Nature-of-Self-Control/Russell-Barkley/9781572303784)

8. Barkley, R.A. (2012). *Executive Functions: What They Are, How They Work, and Why They Evolved.* Guilford Press. [Book](https://www.guilford.com/books/Executive-Functions/Russell-Barkley/9781609189583)

9. Solanto, M.V. (2011). *Cognitive-Behavioral Therapy for Adult ADHD: Targeting Executive Dysfunction.* Guilford Press. [Book](https://www.guilford.com/books/Cognitive-Behavioral-Therapy-for-Adult-ADHD/Mary-Solanto/9781609182249)

10. Sonuga-Barke, E.J.S. (2003). "The dual pathway model of AD/HD." *Neuroscience & Biobehavioral Reviews*, 27(7), 593–604. [DOI: 10.1016/j.neubiorev.2003.08.005](https://doi.org/10.1016/j.neubiorev.2003.08.005)

11. Durand, G. (2020). "Reduced organizational skills in adults with ADHD are due to deficits in persistence, not in strategies." *PeerJ*, 8, e9844. [DOI: 10.7717/peerj.9844](https://doi.org/10.7717/peerj.9844)

### Occupational Functioning & Burnout

12. Barkley, R.A. & Murphy, K.R. (2010). "Impairment in occupational functioning and adult ADHD." *Archives of Clinical Neuropsychology*, 25(3), 157–173. [DOI: 10.1093/arclin/acq014](https://doi.org/10.1093/arclin/acq014)

13. Barkley, R.A. & Fischer, M. (2011). "Predicting impairment in major life activities and occupational functioning." *Developmental Neuropsychology*, 36(2), 137–161. [DOI: 10.1080/87565641.2010.549877](https://doi.org/10.1080/87565641.2010.549877)

14. Fuermaier, A.B.M. et al. (2021). "ADHD at the workplace." *J Neural Transmission*. [DOI: 10.1007/s00702-021-02309-z](https://doi.org/10.1007/s00702-021-02309-z)

15. Langberg, J.M. et al. (2024). "Predicting Occupational Outcomes for Individuals with ADHD." *J Occupational Rehabilitation*. [DOI: 10.1007/s10926-024-10259-y](https://doi.org/10.1007/s10926-024-10259-y)

16. Haverkampf, C. et al. (2024). "Executive function deficits mediate the relationship between employees' ADHD and job burnout." *AIMS Public Health*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11007411/)

17. de Graaf, R. et al. (2008). "The prevalence and effects of adult ADHD on the performance of workers." *Occup Environ Med*, 65(12). [DOI: 10.1136/oem.2007.038448](https://doi.org/10.1136/oem.2007.038448)

18. Lefebvre, P. et al. (2021). "Societal costs of adult ADHD in the United States." *J Managed Care & Specialty Pharmacy*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/)

19. Kessler, R.C. et al. (2005). "Lost work performance due to ADHD." *J Occup Environ Med*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/15951714/)

### ADHD in Tech / Software Engineers

20. Morris, M.R., Begel, A. & Wiedermann, B. (2015). "Understanding the Challenges Faced by Neurodiverse Software Engineering Employees." ACM SIGACCESS. [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/neurodiverse_tech_employees_assets2015.pdf)

21. Liebel, G., Langlois, N. & Gama, K. (2024). "Challenges, Strengths, and Strategies of Software Engineers with ADHD." ACM. [DOI: 10.1145/3639475.3640107](https://doi.org/10.1145/3639475.3640107)

22. McDowall et al. (2025). "Get Me In The Groove: ADHD Programmers and Context Switching." IEEE / UMass. [PDF](https://people.cs.umass.edu/~mendres/papers/GetMeInTheGroove.pdf)

23. Gama, K. et al. (2024). "A Socio-Technical Grounded Theory on Cognitive Dysfunctions in Software Developers with ADHD and Autism." arXiv:2411.13950. [arXiv](https://arxiv.org/abs/2411.13950)

### Prevalence & Epidemiology

24. Song, P. et al. (2021). "The prevalence of adult attention-deficit/hyperactivity disorder: A global meta-analysis." *J Global Health*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/33692893/)

25. Ayano, G. et al. (2023). "Prevalence of ADHD in adults: An umbrella review." *Psychiatry Research*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/37708807/)

26. CDC MMWR, Staley, B. et al. (2024). "Prevalence and Characteristics of Adult ADHD." *MMWR*, 73(40), 890–895. [CDC](https://www.cdc.gov/mmwr/volumes/73/wr/mm7340a2.htm)

27. Das, D. et al. (2012). "A population-based study of ADHD symptoms in middle-aged adults." *PLOS ONE*. [DOI: 10.1371/journal.pone.0034866](https://doi.org/10.1371/journal.pone.0034866)

28. Polanczyk, G. et al. (2007). "The worldwide prevalence of ADHD: a systematic review and metaregression analysis." *American J Psychiatry*, 164(6), 942–948. [DOI: 10.1176/appi.ajp.164.6.942](https://doi.org/10.1176/appi.ajp.164.6.942)

### Context Switching & Attention

29. Mark, G., Gudith, D. & Klocke, U. (2008). "The cost of interrupted work." CHI 2008. [DOI: 10.1145/1357054.1357072](https://doi.org/10.1145/1357054.1357072)

30. Mark, G., Gonzalez, V. & Harris, J. (2005). "No task left behind?" CHI 2005. [DOI: 10.1145/1054972.1055017](https://doi.org/10.1145/1054972.1055017)

31. Leroy, S. (2009). "Why is it so hard to do my work? Attention residue." *OBHDP*, 109(2), 168–181. [DOI: 10.1016/j.obhdp.2009.04.002](https://doi.org/10.1016/j.obhdp.2009.04.002)

32. Rubinstein, J.S., Meyer, D.E. & Evans, J.E. (2001). "Executive Control of Cognitive Processes in Task Switching." *JEP: Human Perception and Performance*, 27(4), 763–797. [APA PsycNet](https://psycnet.apa.org/record/2001-07439-006)

33. Monsell, S. (2003). "Task switching." *Trends in Cognitive Sciences*, 7(3), 134–140. [DOI: 10.1016/S1364-6613(03)00028-7](https://doi.org/10.1016/S1364-6613(03)00028-7)

34. Cepeda, N.J. et al. (2000). "Task Switching and ADHD." *J Abnormal Child Psychology*, 28(3), 213–226. [DOI: 10.1023/A:1005156720754](https://doi.org/10.1023/A:1005156720754)

### Information Overload

35. Arnold, M. et al. (2023). "Dealing with information overload: a comprehensive review." *Frontiers in Psychology*, 14, 1122200. [DOI: 10.3389/fpsyg.2023.1122200](https://doi.org/10.3389/fpsyg.2023.1122200)

36. Roetzel, P.G. (2018). "Information overload in the information age: a review." *Business Research*, 11, 449–466. [DOI: 10.1007/s40685-018-0069-z](https://doi.org/10.1007/s40685-018-0069-z)

37. Eppler, M.J. & Mengis, J. (2004). "The concept of information overload." *The Information Society*, 20(5), 325–344. [DOI: 10.1080/01972240490507974](https://doi.org/10.1080/01972240490507974)

38. Karr-Wisniewski, E. & Lu, Y. (2010). "When more is too much." *Computers in Human Behavior*, 26(5), 1061–1072. [DOI: 10.1016/j.chb.2010.03.008](https://doi.org/10.1016/j.chb.2010.03.008)

### Cognitive Load & Perceptual Load (UI/Design)

39. Le Cunff et al. (2024). "Neurodiversity positively predicts perceived extraneous load." *Education Sciences*, 14(5), 516. [DOI: 10.3390/educsci14050516](https://doi.org/10.3390/educsci14050516)

40. Kasatskii et al. (2023). "Perceptual Load on Performance Within IDE in People with ADHD Symptoms." HCII 2023. [DOI: 10.1007/978-3-031-35017-7_9](https://doi.org/10.1007/978-3-031-35017-7_9)

41. Rosenberg et al. (2023). "Cognitive and perceptual load have opposing effects in ADHD." *Network Neuroscience*, MIT Press, 7(4), 1483. [DOI: 10.1162/netn_a_00341](https://doi.org/10.1162/netn_a_00341)

42. Forster, S. et al. (2014). "Plugging the attention deficit: Perceptual load counters increased distraction in ADHD." *Neuropsychology*, 28(1), 91–97. [DOI: 10.1037/neu0000020](https://doi.org/10.1037/neu0000020)

43. Advokat (2024). "Neurodiversity and cognitive load in online learning: A systematic review." *Computers & Education*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1747938X24000137)

44. Kulsum & Fatima (2025). "Cognitive and attentional barriers in IDEs for ADHD students." *IRE Journals*. [IRE Journals](https://www.irejournals.com/)

### Inclusive & ADHD-Friendly Design

45. Weyerhäuser & Piccolo (2026). "Towards Inclusive Guidelines for Web Design for Adults with ADHD." INTERACT 2025. [DOI: 10.1007/978-3-032-05008-3_59](https://doi.org/10.1007/978-3-032-05008-3_59)

46. Spiel, K. et al. (2022). "ADHD and technology research — investigated by neurodivergent readers." CHI 2022. [DOI: 10.1145/3491102.3517592](https://doi.org/10.1145/3491102.3517592)

47. Leshkov et al. (2024). "Inclusive design principles for neurodivergent individuals." DCC 2024. [DOI: 10.1007/978-3-031-71918-9_10](https://doi.org/10.1007/978-3-031-71918-9_10)

48. Tcherdakoff et al. (2025). "Burnout by design: How digital systems overburden neurodivergent students." CHIWORK 2025. [ACM](https://dl.acm.org/)

49. Edwards et al. (2024). "Visual and auditory distractions in VR for neurodiverse students." *Virtual Reality*, Springer. [DOI: 10.1007/s10055-023-00933-6](https://doi.org/10.1007/s10055-023-00933-6)

### Cognitive Offloading & Scaffolding

50. Gilbert, S.J. et al. (2020). "Optimal use of reminders: Metacognition, effort, and cognitive offloading." *JEP: General*, 149(3), 501–517. [DOI: 10.1037/xge0000652](https://doi.org/10.1037/xge0000652)

51. Gilbert, S.J. et al. (2023). "Outsourcing memory to external tools: A review of 'intention offloading'." *Psychonomic Bulletin & Review*, 30(1), 60–76. [DOI: 10.3758/s13423-022-02139-4](https://doi.org/10.3758/s13423-022-02139-4)

52. Greenwald, M. et al. (2024). "Metacognitive scaffolding for digital reading and mind-wandering in adults with and without ADHD." *Learning and Instruction*, 95, 102051. [DOI: 10.1016/j.learninstruc.2024.102051](https://doi.org/10.1016/j.learninstruc.2024.102051)

53. Weinberger et al. (2023). "Work-MAP Telehealth Metacognitive Work-Performance Intervention for Adults with ADHD: RCT." *OTJR*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10336612/)

54. Zhu, Yu & Luo (2026). "Scaffolding Metacognition with GenAI for ADHD Task Management." CHI 2026. [DOI: 10.1145/3772318](https://doi.org/10.1145/3772318)

55. Katz, Weinberger, Ricon & Rosenblum (2025). "Organization in time, EF, and QoL in adult ADHD." *Brain Sciences*, 15(12), 1262. [DOI: 10.3390/brainsci15121262](https://doi.org/10.3390/brainsci15121262)

### Lived Experience & Qualitative

56. "Work Performance Challenges and Needs of Adults with ADHD" (2025). *European Psychiatry*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12420443/)

57. "I Work Twice as Hard to Look Normal" (2026). *Research Square* (preprint). [Research Square](https://www.researchsquare.com/)

### Intervention Evidence

58. Daley, D. et al. (2025). "Comparative efficacy of interventions for ADHD in adults." *The Lancet Psychiatry* (113 RCTs). [DOI: 10.1016/S2215-0366(24)00360-2](https://doi.org/10.1016/S2215-0366(24)00360-2)

59. An et al. (2025). "Short-term and long-term effect of non-pharmacotherapy for adults with ADHD." Systematic review and NMA. [PubMed](https://pubmed.ncbi.nlm.nih.gov/39958157/)

---

*Sources: PubMed, ACM Digital Library, Springer, MIT Press, CHI proceedings, arXiv, CDC, WHO, PLOS ONE, PeerJ, Frontiers, ScienceDirect, Fortune Business Insights, Stack Overflow Developer Survey, Asana, RescueTime, UC Irvine.*
