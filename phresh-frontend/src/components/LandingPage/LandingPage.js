import React from "react"
import {
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiFlexGroup,
  EuiFlexItem,
} from "@elastic/eui"
import { Carousel, CarouselTitle } from "../../components"
import { useCarousel } from "../../hooks/useCarousel"
import pen from "../../assets/img/120-power-of-pen.svg"
import gymTime from "../../assets/img/103-gym-time.svg"
import macbook from "../../assets/img/118-macbook.svg"
import workFromHome from "../../assets/img/122-work-from-home-2.svg"
import gamingMouse from "../../assets/img/day3-gaming-mouse.svg"
import vintageCamera from "../../assets/img/day7-vintage-camera.svg"
import forklift from "../../assets/img/day14-forklift.svg"
import owl from "../../assets/img/day22-owl.svg"
import styled from "styled-components"

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
  padding-bottom: 5rem;
`
const LandingTitle = styled.h1`
  font-size: 3.5rem;
  margin: 2rem 0;
`

const StyledEuiPageContent = styled(EuiPageContent)`
  border-radius: 50%;
`
const StyledEuiPageContentBody = styled(EuiPageContentBody)`
  max-width: 400px;
  max-height: 400px;

  & > img {
    max-width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
`

const carouselItems = [
  { label: 'gym time', content: <img src={gymTime} alt='gym time' /> },
  { label: 'macbook', content: <img src={macbook} alt='macbook' /> },
  { label: 'work from home', content: <img src={workFromHome} alt='work from home' /> },
  { label: 'gaming mouse', content: <img src={gamingMouse} alt='gaming mouse' /> },
  { label: 'vintage camera', content: <img src={vintageCamera} alt='vintage camera' /> },
  { label: 'forklift', content: <img src={forklift} alt='forklift' /> },
  { label: 'owl', content: <img src={owl} alt='owl' /> },
]

export default function LandingPage() {
  const { current } = useCarousel(carouselItems, 3000)

  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiFlexGroup direction="column" alignItems="center">
          <EuiFlexItem>
            <LandingTitle>Phresh Cleaners</LandingTitle>
          </EuiFlexItem>
          <EuiFlexItem>
            <CarouselTitle items={carouselItems} current={current} />
          </EuiFlexItem>
        </EuiFlexGroup>

        <EuiFlexGroup direction="rowReverse">
          <EuiFlexItem>
            <Carousel items={carouselItems} current={current} />
          </EuiFlexItem>
          <EuiFlexItem>
            <StyledEuiPageContent horizontalPosition="center" verticalPosition="center">
              <StyledEuiPageContentBody>
                <img src={pen} alt="pen" />
              </StyledEuiPageContentBody>
            </StyledEuiPageContent>
          </EuiFlexItem>
        </EuiFlexGroup>
      </EuiPageBody>
    </StyledEuiPage>
  )
}
