import config from '@app/config';
import { faCalendarDays, faCommentDots, faFaceSmile, faFileLines } from '@fortawesome/free-regular-svg-icons';
import { faCaretDown, faLocationDot, faRectangleList, faShieldHalved, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Accordion, AccordionContent, AccordionItem, AccordionToggle, Breadcrumb, BreadcrumbItem, Button, Card, CardBody, Divider, Flex, FlexItem, Grid, GridItem, Label, Page, PageSection, Tab, Tabs, TabTitleText, Text, TextContent, TextVariants, Title } from '@patternfly/react-core';
import axios from 'axios';
import * as React from 'react';
import { useParams } from 'react-router-dom';
import { Chat } from '../Chat/Chat';
import { ImageCarousel } from '../ImageCarousel/ImageCarousel';


interface ClaimProps { }

const ClaimDetail: React.FunctionComponent<ClaimProps> = () => {

  // Claims data
  const { claim_id } = useParams<{ claim_id: string }>();
  const [claim, setClaim] = React.useState<any>({});

  React.useEffect(() => {
    axios.get(config.backend_api_url + `/db/claims/${claim_id}`)
      .then((response) => {
        setClaim(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, [claim_id]);

  // Tabs control
  const [activeTabKey, setActiveTabKey] = React.useState<string | number>(0);
  const [isBox, setIsBox] = React.useState<boolean>(false);
  // Toggle currently active tab
  const handleTabClick = (
    event: React.MouseEvent<any> | React.KeyboardEvent | MouseEvent,
    tabIndex: string | number
  ) => {
    setActiveTabKey(tabIndex);
  };

  // Accordion toggle
  const [expanded, setExpanded] = React.useState(['']);

  const toggle = (id) => {
    const index = expanded.indexOf(id);
    const newExpanded: string[] =
      index >= 0 ? [...expanded.slice(0, index), ...expanded.slice(index + 1, expanded.length)] : [...expanded, id];
    setExpanded(newExpanded);
  };

  // Chat panel
  const [isChatOpen, setIsChatOpen] = React.useState(false);
  const handleChatToggle = (_event: KeyboardEvent | React.MouseEvent) => {
    setIsChatOpen(!isChatOpen);
  };

  // Custom render for the status
  const labelColors = {
    'Processed': 'green',
    'New': 'blue',
  };

  return (
    <Page>
      <PageSection>
        <Breadcrumb ouiaId="BasicBreadcrumb" className='simple-padding'>
          <BreadcrumbItem to="/ClaimsList">&lt; Back to claims</BreadcrumbItem>
        </Breadcrumb>
        <Grid span={12} hasGutter className='padding-top-25'>
          <GridItem span={8}>
            <Card isRounded={true} className='width-100'>
              <CardBody>
                <Flex className='padding-bottom-25'>
                  <FlexItem>
                    <Title headingLevel="h1" size="2xl">
                      <FontAwesomeIcon className='colored-item-blue' icon={faFileLines} />&nbsp;{`${claim.claim_number}`}
                    </Title>
                  </FlexItem>
                  <FlexItem>
                    <Label color={labelColors[String(claim.summary ? 'Processed' : 'New')]}>{claim.summary ? 'Processed' : 'New'}</Label>
                  </FlexItem>
                  <FlexItem align={{ default: 'alignRight' }}>
                    <TextContent>
                      <Text className='colored-item-blue'>
                        <FontAwesomeIcon icon={faUser} />&nbsp;{claim.client_name ? claim.client_name : 'No client name specified'}
                      </Text>
                    </TextContent>
                  </FlexItem>
                  <Divider
                    orientation={{
                      default: 'vertical'
                    }}
                  />
                  <FlexItem>
                    <TextContent>
                      <Text className='colored-item-blue'>
                        <FontAwesomeIcon icon={faShieldHalved} />&nbsp;{claim.policy_number ? claim.policy_number : 'No policy number specified'}
                      </Text>
                    </TextContent>
                  </FlexItem>
                  <FlexItem>
                    <Button className="disabled-link" variant="primary" isDisabled={true}>Edit</Button>
                  </FlexItem>
                </Flex>
                <Flex>
                  <FlexItem className='width-100'>
                    <Tabs
                      activeKey={activeTabKey}
                      onSelect={handleTabClick}
                      isBox={isBox}
                      aria-label="Tab navigation"
                      role="region"
                    >
                      <Tab eventKey={0} title={<TabTitleText>Summary</TabTitleText>} aria-label="Summary">
                        <Grid span={12} hasGutter>
                          <GridItem span={1} className='padding-top-25'>
                            <FontAwesomeIcon icon={faCalendarDays} className='icon-circle' />
                          </GridItem >
                          <GridItem span={11} className='padding-top-25'>
                            <TextContent>
                              <Text component={TextVariants.h3}>Date and time</Text>
                              <Text>{claim.time ? claim.time : 'Not processed yet'}</Text>
                            </TextContent>
                          </GridItem>
                          <GridItem span={1} className='padding-top-25'>
                            <FontAwesomeIcon icon={faLocationDot} className='icon-circle' />
                          </GridItem >
                          <GridItem span={11} className='padding-top-25'>
                            <TextContent>
                              <Text component={TextVariants.h3}>Location of event</Text>
                              <Text>{claim.location ? claim.location : 'Not processed yet'}</Text>
                            </TextContent>
                          </GridItem>
                          <GridItem span={1} className='padding-top-25'>
                            <FontAwesomeIcon icon={faRectangleList} className='icon-circle' />
                          </GridItem >
                          <GridItem span={11} className='padding-top-25'>
                            <TextContent>
                              <Text component={TextVariants.h3}>Summary</Text>
                              <Text>{claim.summary ? claim.summary : 'Not processed yet'}</Text>
                            </TextContent>
                          </GridItem>
                          <GridItem span={1} className='padding-top-25'>
                            <FontAwesomeIcon icon={faFaceSmile} className='icon-circle' />
                          </GridItem >
                          <GridItem span={11} className='padding-top-25'>
                            <TextContent>
                              <Text component={TextVariants.h3}>Customer Sentiment</Text>
                              <Text>{claim.sentiment ? claim.sentiment : 'Not processed yet'}</Text>
                            </TextContent>
                          </GridItem>
                        </Grid>
                      </Tab>
                      <Tab eventKey={1} title={<TabTitleText>Insurance</TabTitleText>} aria-label="Insurance" isDisabled></Tab>
                      <Tab eventKey={2} title={<TabTitleText>Damages</TabTitleText>} aria-label="Damages" isDisabled></Tab>
                      <Tab eventKey={3} title={<TabTitleText>Witnesses</TabTitleText>} aria-label="Witnesses" isDisabled></Tab>
                      <Tab eventKey={4} title={<TabTitleText>Documents</TabTitleText>} aria-label="Documents">
                        <Accordion isBordered asDefinitionList={false} className='padding-top-25'>
                          <AccordionItem>
                            <AccordionToggle
                              onClick={() => toggle('claim-toggle1')}
                              isExpanded={expanded.includes('claim-toggle1')}
                              id="claim-toggle1">
                              Original claim content
                            </AccordionToggle>
                            <AccordionContent id="claim-content1" isHidden={expanded.includes('claim-toggle1')}>
                              <TextContent>
                                <Text component={TextVariants.h3}>Subject:</Text>
                                {claim.subject}
                                <Text component={TextVariants.h3}>Body:</Text>
                                <div className='display-linebreak'>{claim.body}</div>
                                <Text component={TextVariants.h3}>Attached images:</Text>
                                {claim && claim.original_images && <Grid><GridItem span={4}><ImageCarousel images={claim.original_images} /></GridItem></Grid>}
                              </TextContent>
                            </AccordionContent>
                          </AccordionItem>
                        </Accordion>
                      </Tab>
                      <Tab eventKey={5} title={<TabTitleText>Comments</TabTitleText>} aria-label="Comments" isDisabled></Tab>
                    </Tabs>
                  </FlexItem>
                </Flex>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem span={4}>
            <Card isRounded={true} className='width-100'>
              <CardBody>
                {(claim && claim.processed_images) ? <ImageCarousel images={claim.processed_images} /> : 'No images attached'}
              </CardBody>
            </Card>
          </GridItem>
        </Grid>
        <Flex >
          <FlexItem>
            <Button variant="link" onClick={handleChatToggle} className='icon-chat-button' aria-label='OpenChat'>
              {!isChatOpen ? <FontAwesomeIcon icon={faCommentDots} className='icon-chat' /> : <FontAwesomeIcon icon={faCaretDown} className='icon-chat' />}
            </Button>
          </FlexItem>
        </Flex>
        <Flex className={isChatOpen ? 'chat-fadeIn' : 'chat-fadeOut'}>
          <FlexItem className='chat-panel'><Chat claimSummary={claim.summary}/></FlexItem>
        </Flex>
      </PageSection>
    </Page>
  );
}

export { ClaimDetail };
