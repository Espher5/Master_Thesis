# Master_Thesis

In this thesis, we design and conduct two experiments (i.e., a baseline and its
replication), with the participation of final year Master’s degree students in Computer
Science, and present their results; the goal of these experiments is to compare Test-
Driven Development (TDD), an incremental approach to software development where
tests are written before production code, with a traditional way of testing where
production code is written before tests (i.e., NO-TDD). TDD has been the subject of
numerous studies over the years, with the purpose of determining whether applying
this technique would result in an improved development: in this study, TDD and
NO-TDD have been contrasted in the context of the implementation of Embedded
Systems (ESs). During the baseline experiment we provided the participants with
two ESs to implement and test in a host development environment, while mocking
the underlying hardware platform. As for the replication study, its main goal is
to validate the results obtained from the baseline experiment and to generalize
them to a different and more real setting. In particular, during the replication
experiment, we asked participants to implement another ES, which this time had
to be effectively deployed and tested on a hardware platform (i.e., a Raspberry
Pi model 4). Given the small number of participants to this study, we consider
this assessment the first exploratory step to the research on the topic of TDD for
ESs, given the fact that there are no similar studies available yet. As a result, the
gathered data cannot prove a statistically significant difference between the two
approaches; however, this data provided interesting cues to determine where to head
with a future, more extensive, research on the topic. From the two experiments we
gathered quantitative data; moreover, qualitative data was also gathered to explain
the quantitative measurements obtained, and to provide a better understanding of
the phenomenon under study. After the analysis, data suggests that the external
quality of the developed implementation and number of written test cases increase
when using TDD to develop ESs, while there is not a substantial difference with
respect to the developers’ productivity. Finally, developers’ perspectives highlight
how TDD is perceived as a more difficult approach to apply compared to NO-TDD.