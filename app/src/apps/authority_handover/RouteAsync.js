// import asyncComponent from './asyncComponent';
import asyncRoute from './asyncComponent';


export { default as App } from '../app'
export const CollegeList = asyncRoute(() => System.import('../apps/college/CollegeList'));
export const CouncilDetail = asyncRoute(() => System.import('../apps/council/CouncilDetail'));

// export const App = asyncComponent(() => import('../app')
//   .then(module => module.default));
// export const CollegeList = asyncComponent(() => import('../apps/college/CollegeList')
//   .then(module => module.default));
// export const CollegeDetail = asyncComponent(() => import('../apps/college/CollegeDetail')
//   .then(module => module.default));
// export const CourseList = asyncComponent(() => import('../apps/course/CourseList')
//   .then(module => module.default));
// export const CourseDetail = asyncComponent(() => import('../apps/course/CourseDetail')
//   .then(module => module.default));
// export const UniversityList = asyncComponent(() => import('../apps/university/UniversityList')
//   .then(module => module.default));
// export const UniversityDetail = asyncComponent(() => import('../apps/university/UniversityDetail')
//   .then(module => module.default));
// export const AdmissionList = asyncComponent(() => import('../apps/admission/AdmissionList')
//   .then(module => module.default));
// export const AdmissionDetail = asyncComponent(() => import('../apps/admission/AdmissionDetail')
//   .then(module => module.default));
// export const CareerList = asyncComponent(() => import('../apps/career/CareerList')
//   .then(module => module.default));
// export const CareerDetail = asyncComponent(() => import('../apps/career/CareerDetail')
//   .then(module => module.default));
// export const EventList = asyncComponent(() => import('../apps/event/EventList')
//   .then(module => module.default));
// export const EventDetail = asyncComponent(() => import('../apps/event/EventDetail')
//   .then(module => module.default));
// export const NewsList = asyncComponent(() => import('../apps/news/NewsList')
//   .then(module => module.default));
// export const NewsDetail = asyncComponent(() => import('../apps/news/NewsDetail')
//   .then(module => module.default));
// export const ScholarshipList = asyncComponent(() => import('../apps/scholarship/ScholarshipList')
//   .then(module => module.default));
// export const ScholarshipDetail = asyncComponent(() => import('../apps/scholarship/ScholarshipDetail')
//   .then(module => module.default));
// export const VacancyList = asyncComponent(() => import('../apps/vacancy/VacancyList')
//   .then(module => module.default));
// export const VacancyDetail = asyncComponent(() => import('../apps/vacancy/VacancyDetail')
//   .then(module => module.default));
// export const CategoryList = asyncComponent(() => import('../apps/categories/CategoryList')
//   .then(module => module.default));
// export const RankList = asyncComponent(() => import('../apps/rank/RankList')
//   .then(module => module.default));
// export const RankDetail = asyncComponent(() => import('../apps/rank/RankDetail')
//   .then(module => module.default));
// export const FacultyCourseList = asyncComponent(() => import('../apps/faculty/FacultyCourseList')
//   .then(module => module.default));
// export const LoginForm = asyncComponent(() => import('../apps/users/components/LoginForm')
//   .then(module => module.default));
// export const SignUpForm = asyncComponent(() => import('../apps/users/components/SignUpForm')
//   .then(module => module.default));
// export const Header = asyncComponent(() => import('../components/Header')
//   .then(module => module.default));
// export const Footer = asyncComponent(() => import('../components/Footer')
//   .then(module => module.default));
// export const LoadingComponent = asyncComponent(() => import('./LoadingComponent')
//   .then(module => module.default));
// export const ShortList = asyncComponent(() => import('./ShortList')
//   .then(module => module.default));
// export const PageDetail = asyncComponent(() => import('../apps/page/PageDetail')
//   .then(module => module.default));
// export const SearchList = asyncComponent(() => import('../apps/search/SearchList')
//   .then(module => module.default));
// export const CouncilList = asyncComponent(() => import('../apps/council/CouncilList')
//   .then(module => module.default));
// export const CouncilDetail = asyncComponent(() => import('../apps/council/CouncilDetail')
//   .then(module => module.default));