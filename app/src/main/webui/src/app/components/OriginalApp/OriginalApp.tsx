import * as React from 'react';
import { Page, PageSection, TextContent, Text, TextVariants, Title, Tabs, Tab } from '@patternfly/react-core';
import car1 from '@app/assets/images/car1.jpg';
import car2 from '@app/assets/images/car2.jpg';
import car3 from '@app/assets/images/car3.jpg';
import ocar0 from '@app/assets/images/original_car0.jpg';
import ocar1 from '@app/assets/images/original_car1.jpg';
import ocar2 from '@app/assets/images/original_car2.jpg';
import ocar3 from '@app/assets/images/original_car3.jpg';
import ocar4 from '@app/assets/images/original_car4.jpg';
import ocar5 from '@app/assets/images/original_car5.jpg';
import ocar6 from '@app/assets/images/original_car6.jpg';
import pcar0 from '@app/assets/images/car0-processed.jpg';
import pcar1 from '@app/assets/images/car1-processed.jpg';
import pcar2 from '@app/assets/images/car2-processed.jpg';
import pcar3 from '@app/assets/images/car3-processed.jpg';
import pcar4 from '@app/assets/images/car4-processed.jpg';
import pcar5 from '@app/assets/images/car5-processed.jpg';
import pcar6 from '@app/assets/images/car6-processed.jpg';

const OriginalApp: React.FunctionComponent = () => {
  const [activeTabKey, setActiveTabKey] = React.useState<string | number>(0);
  const [isBox, setIsBox] = React.useState<boolean>(false);
  // Toggle currently active tab
  const handleTabClick = (
    event: React.MouseEvent<any> | React.KeyboardEvent | MouseEvent,
    tabIndex: string | number
  ) => {
    setActiveTabKey(tabIndex);
  };
  const toggleBox = (checked: boolean) => {
    setIsBox(checked);
  };
  return (
    <Page>
      <PageSection>
        <Title headingLevel="h1" size="lg">Received Claims</Title>
      </PageSection>
      <PageSection>
        <Tabs activeKey={activeTabKey}
          onSelect={handleTabClick}
          isBox={isBox}
          aria-label="Tabs in the default example"
          role="region">
          <Tab title="Claim 1" eventKey={0}>
            <TextContent className="pf-v5-u-font-size-xs">
              <Text component={TextVariants.h3}>Subject:</Text>
              <p>Claim for Recent Car Accident - Policy Number: ABC12345</p>
              <Text component={TextVariants.h3}>Body:</Text>
              <p>Dear XYZ Insurance Company,</p>
              <p>I hope this email finds you well. I am writing to report a recent car accident in
                which I was involved, and I would like to initiate a claim under my policy with your company. My policy
                number is ABC12345, and my name is John Smith.</p>
              <p>Accident Details:</p>
              <p>Date and Time: The accident occurred on October 15, 2023, at approximately 2:30
                PM.</p>
              <p>Location: The accident took place at the intersection of Elm Street and Maple Avenue,
                near Smith Park, in Springfield, Illinois. The exact coordinates are 39.7476&deg; N, 89.6960&deg; W.
              </p>
              <p>Circumstances:</p>
              <p>1. Weather Conditions: On the day of the accident, the weather was overcast with
                light rain. The road was wet.</p>
              <p>2. Traffic Conditions: Traffic was moderate at the time, with vehicles traveling in
                all directions. I was driving at the posted speed limit of 35 mph.</p>
              <p>3. Vehicle Involved: I was driving my Honda Accord at the time of the accident. The
                other party involved was driving a Ford Escape.</p>
              <p>4. Sequence of Events: While I was proceeding through the intersection with a green
                light, the other vehicle, which was coming from the north, ran a red light and collided with the front
                passenger side of my vehicle. I had no time to react to avoid the collision.</p>
              <p>5. Injuries: Thankfully, there were no serious injuries, but both vehicles sustained
                significant damage. The police were called to the scene, and a report was filed. The officer&#39;s badge
                number is 12345, and I can provide a copy of the accident report upon request.</p>
              <p>6. Witness Information: There were a few witnesses to the accident, and I have their
                contact information. Their names are Sarah Johnson, Mark Williams, and Lisa Anderson.</p>
              <p>7. Photos: I have taken several photos of the accident scene, including the damage to
                both vehicles, the traffic signals, and road conditions. I can provide these photos to assist with the
                claim.</p>
              <p>8. Other Party&#39;s Information: The driver of the other vehicle provided me with
                their insurance information and contact details, which I can share with you.</p>
              <p>Claim Request:</p>
              <p>I would like to request that you initiate a claim under my policy for the damages to
                my vehicle. I would appreciate it if you could provide me with the next steps and the claim process. Please
                let me know what documentation or information you require from me to process this claim efficiently.
              </p>
              <p>I understand that accidents happen, and I trust in your company&#39;s ability to
                assist me during this challenging time. Your prompt attention to this matter is greatly appreciated.
              </p>
              <p>Please contact me at (555) 123-4567 or john.smith@email.com to discuss this further
                or to request any additional information you may need.</p>
              <p>Thank you for your assistance in this matter, and I look forward to your prompt
                response.</p>
              <p>Sincerely,</p>
              <p>John Smith</p>
              <Text component={TextVariants.h3}>Attached images:</Text>
            </TextContent>
            <img src={car1} width={250} />
          </Tab>
          <Tab title="Claim 2" eventKey={1}>
            <TextContent>
              <Text component={TextVariants.h3}>Subject:</Text>
              <p>URGENT - Car Accident Claim - Policy Number: ABC12345</p>
              <Text component={TextVariants.h3}>Body:</Text>
              <p>To Whom It May Concern at XYZ Insurance Company,</p>
              <p>I can&#39;t believe I have to go through the hassle of contacting you regarding a car
                accident claim, but I guess that&#39;s why I pay for insurance, right? My policy number is ABC12345, and my
                name is John Smith.</p>
              <p>Accident Details:</p>
              <p>Date and Time: This whole nightmare happened on October 15, 2023, at around 2:30
                PM.</p>
              <p>Location: The accident took place at the intersection of Elm Street and Maple Avenue,
                near Smith Park in Springfield, Illinois. I even provided the exact coordinates: 39.7476&deg; N,
                89.6960&deg; W. The least you could do is use a map.</p>
              <p>Circumstances:</p>
              <p>1. Weather Conditions: The weather? Oh, it was just lovely. Overcast with some light
                rain. The road? It was wet, alright.</p>
              <p>2. Traffic Conditions: I had the privilege of navigating through moderate traffic,
                with vehicles going in all directions. I was going exactly 35 mph, in case you care.</p>
              <p>3. Vehicle Involved: My beloved Honda Accord was involved. The other party was
                driving a Ford Escape.</p>
              <p>4. Sequence of Events: Listen up &ndash; I was cruising through the intersection with
                a green light, minding my own business. Then, this genius coming from the north decided that red lights
                don&#39;t apply to them and plowed into my passenger side. I didn&#39;t have time to react, thanks to their
                stupidity.</p>
              <p>5. Injuries: Thankfully, we all walked away without injuries, but the vehicles? They
                weren&#39;t so lucky. Of course, the police showed up and filed a report. Badge number 12345, as if that
                means anything to me. Get me the report if you want it so badly.</p>
              <p>6. Witness Information: Yeah, there were witnesses. Sarah Johnson, Mark Williams, and
                Lisa Anderson, to be exact. Get in touch with them, not me!</p>
              <p>7. Photos: I went the extra mile to document everything. I&#39;ve got photos of the
                accident scene, the vehicle damage, traffic lights &ndash; you name it. You can&#39;t accuse me of not being
                prepared.</p>
              <p>8. Other Party&#39;s Information: The other driver handed over their insurance info
                and contact details. I suppose you want that too?</p>
              <p>Claim Request:</p>
              <p>I don&#39;t have time for games. I want to initiate a claim for the damage to my car,
                and I want it done yesterday. Tell me the process, give me the paperwork, and let&#39;s get this over with.
                I&#39;ve got a life to live, and this accident is just a roadblock.</p>
              <p>I trust you&#39;ll act swiftly to address this matter. I don&#39;t want excuses; I
                want results. Reach me at (555) 123-4567 or john.smith@email.com. I don&#39;t care if it&#39;s after hours
                &ndash; make it happen.</p>
              <p>I&#39;m not here to make friends. I&#39;m here for the insurance I&#39;ve been paying
                for, so get your act together and give me a prompt response.</p>
              <p>Sincerely,</p>
              <p>John Smith</p>
              <Text component={TextVariants.h3}>Attached images:</Text>
            </TextContent>
            <img src={car2} width={250} />
          </Tab>
          <Tab title="Claim 3" eventKey={2}>
            <TextContent>
              <Text component={TextVariants.h3}>Subject:</Text>
              <p>I Need Help with Car Accident Claim - My Policy is ABC12345</p>
              <Text component={TextVariants.h3}>Body:</Text>
              <p>Hi there, XYZ Insurance Company,</p>
              <p>I hope this email is okay and finds you okay. I had an accident, and I&#39;m not
                exactly sure how to go about this, but I think it&#39;s something to do with a car accident claim, and my
                policy number is ABC12345, I think.</p>
              <p>Okay, so here&#39;s what happened:</p>
              <p>Accident Stuff:</p>
              <p>Date and Time: Um, so this accident thing happened on, like, October 15th, 2023, at,
                um, 2:30 PM, I think.</p>
              <p>Location: So, it happened at this place, um, the intersection of Elm Street and Maple
                Avenue, near Smith Park in Springfield, Illinois. I heard you might need some coordinates? They&#39;re like
                39.7476&deg; N and 89.6960&deg; W or something. Hope that helps.</p>
              <p>The Accidenty Part:</p>
              <p>Weather Conditions: Well, the weather was kinda not great, I guess. It was like,
                cloudy and a bit rainy. And the road was wet, you know?</p>
              <p>Traffic Conditions: There were some cars around, like, moderate traffic, I guess. And
                I was driving, like, the speed limit, which is, um, 35 mph, I think.</p>
              <p>Car Details: So, my car is a Honda Accord, I think, and the other car involved was a
                Ford Escape. Yeah, that&#39;s right.</p>
              <p>What Happened: So, I had the green light, and I was driving through the intersection,
                you know? But the other car, coming from the north or something, ran a red light and hit the front of my car
                on the passenger side. I didn&#39;t really have time to react or anything.</p>
              <p>Injuries: Good news, no one got hurt really bad, but our cars got pretty messed up.
                The police came and made a report, and the officer had a badge number, I guess, it&#39;s 12345. I can get
                you the report if you need it.</p>
              <p>Witness Stuff: There were a few people who saw this happen, and I got their names.
                It&#39;s Sarah Johnson, Mark Williams, and Lisa Anderson.</p>
              <p>Photos: I took some pictures at the scene, like of the cars, the traffic lights, and
                the road and stuff. If you want to see them, just let me know.</p>
              <p>Other Driver Info: The other driver gave me their insurance info and contact stuff,
                so I can share that with you too.</p>
              <p>Now, um, about the claim:</p>
              <p>I guess I need to do something about this, right? Can you help me with the steps and
                what I need to give you? I don&#39;t really know how these things work.</p>
              <p>I know accidents happen, and, uh, I hope you can help me through this. Can you reply
                quickly, please? I&#39;d really appreciate it.</p>
              <p>You can call me at (555) 123-4567 or email me at john.smith@email.com. I&#39;m not
                really good at this stuff, so, you know, thanks for your help.</p>
              <p>Sincerely,</p>
              <p>John Smith</p>
              <Text component={TextVariants.h3}>Attached images:</Text>
            </TextContent>
            <img src={car3} width={250} />
            <img src={ocar0} width={250} />
            <img src={ocar1} width={250} />
            <img src={ocar2} width={250} />
            <img src={ocar3} width={250} />
            <img src={ocar4} width={250} />
            <img src={ocar5} width={250} />
            <img src={ocar6} width={250} />
            <img src={pcar0} width={250} />
            <img src={pcar1} width={250} />
            <img src={pcar2} width={250} />
            <img src={pcar3} width={250} />
            <img src={pcar4} width={250} />
            <img src={pcar5} width={250} />
            <img src={pcar6} width={250} />
          </Tab>
        </Tabs>
      </PageSection>
    </Page>
  )
}

export { OriginalApp };
